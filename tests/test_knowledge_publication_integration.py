import hashlib
import uuid
from dataclasses import replace
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy import delete, select
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.modules.auth.models import User, UserRole
from app.modules.knowledge.bangladesh_demo_pack import (
    get_draft_guides,
)
from app.modules.knowledge.models import (
    KnowledgeChunk,
    KnowledgePublicationAudit,
    KnowledgeLanguage,
)
from app.modules.knowledge.publication import (
    ClaimEvidence,
    KnowledgePublicationService,
)
from app.modules.knowledge.source_review import (
    KnowledgeSourceReview,
)


pytestmark = pytest.mark.anyio

# Synthetic vector. No Gemini API calls.
TEST_VECTOR = [1.0] + [0.0] * 767

# Test metadata, not verified government evidence.
TEST_SOURCE_URL = "https://bdris.gov.bd/br/correction"

APPROVED_CONTENT = (
    "This is synthetic integration-test knowledge. "
    "It does not describe a real government procedure. "
    "The purpose is to test atomic database publication."
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def publication_context():
    production_url = make_url(settings.DATABASE_URL)

    if production_url.database != "jonoseba_db":
        raise RuntimeError(
            "Unexpected DATABASE_URL. "
            "Refusing to run publication integration tests."
        )

    test_url = production_url.set(
        database="jonoseba_test_db"
    )

    if test_url.database != "jonoseba_test_db":
        raise RuntimeError(
            "Integration tests require jonoseba_test_db."
        )

    engine = create_async_engine(test_url)

    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    try:
        async with session_factory() as db:
            unique_id = uuid.uuid4().hex

            admin = User(
                full_name="Knowledge Test Admin",
                email=f"knowledge-{unique_id}@example.org",
                hashed_password="test-only-not-a-real-password",
                role=UserRole.ADMIN,
                is_active=True,
            )

            db.add(admin)
            await db.commit()
            await db.refresh(admin)

            # Save scalar ID before any rollback.
            # This prevents MissingGreenlet in teardown.
            admin_id = admin.id

            draft = replace(
                get_draft_guides()[0],
                document_key=f"atomic-test-{unique_id}",
            )

            review = KnowledgeSourceReview(
                document_key=draft.document_key,
                source_url=TEST_SOURCE_URL,
                source_name="Integration Test Source",
                reviewed_at=datetime.now(timezone.utc),
                reviewed_flags=draft.review_flags,
                evidence_notes=(
                    "Synthetic evidence for testing database "
                    "transactions, not actual government approval."
                ),
            )

            evidence = tuple(
                ClaimEvidence(
                    review_flag=flag,
                    source_url=TEST_SOURCE_URL,
                    source_excerpt=(
                        "Synthetic integration-test evidence "
                        f"for review requirement: {flag}"
                    ),
                    source_text=(
                        "This is synthetic source material for "
                        "database transaction integration testing. "
                        "Synthetic integration-test evidence "
                        f"for review requirement: {flag}"
                    ),
                )
                for flag in draft.review_flags
            )

            embeddings = MagicMock()
            embeddings.embed_document = AsyncMock(
                return_value=TEST_VECTOR
            )

            service = KnowledgePublicationService(
                db=db,
                embedding_service=embeddings,
            )

            try:
                yield {
                    "db": db,
                    "admin": admin,
                    "draft": draft,
                    "review": review,
                    "evidence": evidence,
                    "service": service,
                }

            finally:
                # Clean up only records belonging to this test.
                await db.rollback()

                await db.execute(
                    delete(KnowledgePublicationAudit).where(
                        KnowledgePublicationAudit.document_key
                        == draft.document_key
                    )
                )

                await db.execute(
                    delete(KnowledgeChunk).where(
                        KnowledgeChunk.document_key
                        == draft.document_key
                    )
                )

                await db.execute(
                    delete(User).where(
                        User.id == admin_id
                    )
                )

                await db.commit()

    finally:
        await engine.dispose()


def publication_args(context, reviewer=None):
    return {
        "draft": context["draft"],
        "review": context["review"],
        "reviewer": (
            reviewer
            if reviewer is not None
            else context["admin"]
        ),
        "approved_content": APPROVED_CONTENT,
        "evidence": context["evidence"],
    }


async def load_chunks(db, document_key):
    result = await db.execute(
        select(KnowledgeChunk)
        .where(
            KnowledgeChunk.document_key
            == document_key
        )
        .order_by(KnowledgeChunk.chunk_index)
    )

    return result.scalars().all()


async def load_audits(db, document_key):
    result = await db.execute(
        select(KnowledgePublicationAudit).where(
            KnowledgePublicationAudit.document_key
            == document_key
        )
    )

    return result.scalars().all()


async def test_real_publication_saves_chunks_and_audit(
    publication_context,
):
    context = publication_context
    db = context["db"]
    draft = context["draft"]

    result = await context["service"].publish(
        **publication_args(context)
    )

    chunks = await load_chunks(
        db,
        draft.document_key,
    )

    audits = await load_audits(
        db,
        draft.document_key,
    )

    assert result["is_published"] is True
    assert result["chunk_count"] == len(chunks)
    assert len(chunks) >= 1
    assert all(chunk.is_published for chunk in chunks)

    assert len(audits) == 1

    audit = audits[0]

    assert audit.reviewer_id == context["admin"].id
    assert audit.source_url == TEST_SOURCE_URL

    expected_hash = hashlib.sha256(
        APPROVED_CONTENT.encode("utf-8")
    ).hexdigest()

    assert audit.approved_content_sha256 == expected_hash

    assert len(audit.claim_evidence) == len(
        draft.review_flags
    )

    # New evidence-matching audit data.
    expected_source_hash = hashlib.sha256(
        context["evidence"][0].source_text.encode("utf-8")
    ).hexdigest()

    assert (
        audit.claim_evidence[0]["source_text_sha256"]
        == expected_source_hash
    )


async def test_audit_failure_rolls_back_new_chunks(
    publication_context,
):
    context = publication_context
    db = context["db"]
    draft = context["draft"]

    # Passes service-level role check but is
    # not a real database user.
    invalid_reviewer = SimpleNamespace(
        id=-999999,
        role=UserRole.ADMIN,
        is_active=True,
    )

    with pytest.raises(IntegrityError):
        await context["service"].publish(
            **publication_args(
                context,
                reviewer=invalid_reviewer,
            )
        )

    chunks = await load_chunks(
        db,
        draft.document_key,
    )

    audits = await load_audits(
        db,
        draft.document_key,
    )

    assert chunks == []
    assert audits == []


async def test_failed_republication_preserves_old_chunks(
    publication_context,
):
    context = publication_context
    db = context["db"]
    draft = context["draft"]

    old_content = (
        "Previously published synthetic knowledge "
        "that must survive a failed replacement."
    )

    old_chunk = KnowledgeChunk(
        document_key=draft.document_key,
        document_title="Previous Test Document",
        chunk_index=0,
        content=old_content,
        language=KnowledgeLanguage.ENGLISH,
        source_url=TEST_SOURCE_URL,
        source_name="Previous Test Source",
        verified_at=datetime.now(timezone.utc),
        is_published=True,
        embedding=TEST_VECTOR,
    )

    db.add(old_chunk)
    await db.commit()

    old_chunk_id = old_chunk.id

    invalid_reviewer = SimpleNamespace(
        id=-999999,
        role=UserRole.ADMIN,
        is_active=True,
    )

    with pytest.raises(IntegrityError):
        await context["service"].publish(
            **publication_args(
                context,
                reviewer=invalid_reviewer,
            )
        )

    chunks = await load_chunks(
        db,
        draft.document_key,
    )

    audits = await load_audits(
        db,
        draft.document_key,
    )

    assert len(chunks) == 1
    assert chunks[0].id == old_chunk_id
    assert chunks[0].content == old_content
    assert chunks[0].is_published is True
    assert audits == []
