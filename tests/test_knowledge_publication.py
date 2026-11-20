import hashlib
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import pytest
from app.modules.auth.models import UserRole
from app.modules.knowledge.bangladesh_demo_pack import (
    get_draft_guides,
)
from app.modules.knowledge.models import (
    KnowledgePublicationAudit,
)
from app.modules.knowledge.publication import (
    ClaimEvidence,
    KnowledgePublicationService,
)
from app.modules.knowledge.source_review import (
    KnowledgeSourceReview,
)


pytestmark = pytest.mark.anyio

SOURCE_URL = "https://bdris.gov.bd/br/correction"

APPROVED_CONTENT = (
    "জন্মনিবন্ধনের সংশোধনের জন্য সংশ্লিষ্ট "
    "নিবন্ধক কার্যালয়ের নির্দেশনা অনুসরণ করতে হবে। "
    "নির্দিষ্ট শর্ত ও প্রমাণপত্র অফিসিয়াল "
    "নির্দেশিকার সঙ্গে মিলিয়ে নিতে হবে।"
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def draft():
    return get_draft_guides()[0]


@pytest.fixture
def admin():
    return SimpleNamespace(
        id=1,
        role=UserRole.ADMIN,
        is_active=True,
    )


@pytest.fixture
def review(draft):
    return KnowledgeSourceReview(
        document_key=draft.document_key,
        source_url=SOURCE_URL,
        source_name="Registration Authority",
        reviewed_at=datetime.now(timezone.utc),
        reviewed_flags=draft.review_flags,
        evidence_notes=(
            "Reviewer examined the source and checked "
            "the applicable guidance against the draft."
        ),
    )


@pytest.fixture
def evidence(draft):
    return tuple(
        ClaimEvidence(
            review_flag=flag,
            source_url=SOURCE_URL,
            source_excerpt=(
                "Test-only source excerpt representing "
                f"review evidence for: {flag}"
            ),
            source_text=(
                "This is synthetic source text used only "
                "for publication unit testing. "
                "Test-only source excerpt representing "
                f"review evidence for: {flag}"
            ),
        )
        for flag in draft.review_flags
    )


@pytest.fixture
def service():
    db = MagicMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()

    instance = KnowledgePublicationService(
        db=db,
        embedding_service=MagicMock(),
    )

    instance.ingestion.ingest_document = AsyncMock(
        return_value={
            "document_key": "bd-birth-registration-new",
            "chunk_count": 2,
            "language": "bn",
            "is_published": True,
        }
    )

    return instance


def request_data(draft, review, admin, evidence):
    return {
        "draft": draft,
        "review": review,
        "reviewer": admin,
        "approved_content": APPROVED_CONTENT,
        "evidence": evidence,
    }


async def test_reviewed_document_is_sent_to_ingestion(
    service, draft, review, admin, evidence
):
    result = await service.publish(
        **request_data(draft, review, admin, evidence)
    )

    assert result["is_published"] is True

    service.ingestion.ingest_document.assert_awaited_once()

    call = service.ingestion.ingest_document.await_args
    document = call.args[0]

    assert document.content == APPROVED_CONTENT
    assert document.is_published is True
    assert document.source_url == SOURCE_URL
    assert call.kwargs == {"commit": False}

    service.db.commit.assert_awaited_once()
    service.db.rollback.assert_not_awaited()


async def test_citizen_cannot_publish(
    service, draft, review, admin, evidence
):
    admin.role = UserRole.CITIZEN

    with pytest.raises(PermissionError):
        await service.publish(
            **request_data(draft, review, admin, evidence)
        )

    service.ingestion.ingest_document.assert_not_awaited()
    service.db.commit.assert_not_awaited()


async def test_missing_evidence_is_rejected(
    service, draft, review, admin, evidence
):
    data = request_data(draft, review, admin, evidence)
    data["evidence"] = evidence[:-1]

    with pytest.raises(
        ValueError,
        match="every draft",
    ):
        await service.publish(**data)

    service.ingestion.ingest_document.assert_not_awaited()
    service.db.commit.assert_not_awaited()


async def test_duplicate_evidence_is_rejected(
    service, draft, review, admin, evidence
):
    data = request_data(draft, review, admin, evidence)
    data["evidence"] = evidence + (evidence[0],)

    with pytest.raises(
        ValueError,
        match="every draft",
    ):
        await service.publish(**data)

    service.ingestion.ingest_document.assert_not_awaited()
    service.db.commit.assert_not_awaited()


async def test_mismatched_evidence_url_is_rejected(
    service, draft, review, admin, evidence
):
    incorrect = ClaimEvidence(
        review_flag=evidence[0].review_flag,
        source_url="https://other.gov.bd/notice",
        source_excerpt=evidence[0].source_excerpt,
        source_text=evidence[0].source_text,
    )

    data = request_data(draft, review, admin, evidence)
    data["evidence"] = (incorrect,) + evidence[1:]

    with pytest.raises(
        ValueError,
        match="source URL",
    ):
        await service.publish(**data)

    service.ingestion.ingest_document.assert_not_awaited()
    service.db.commit.assert_not_awaited()


async def test_original_draft_cannot_be_published(
    service, draft, review, admin, evidence
):
    data = request_data(draft, review, admin, evidence)
    data["approved_content"] = draft.content

    with pytest.raises(
        ValueError,
        match="rewritten",
    ):
        await service.publish(**data)

    service.ingestion.ingest_document.assert_not_awaited()
    service.db.commit.assert_not_awaited()


async def test_short_excerpt_is_rejected(
    service, draft, review, admin, evidence
):
    incorrect = ClaimEvidence(
        review_flag=evidence[0].review_flag,
        source_url=SOURCE_URL,
        source_excerpt="Short",
        source_text=evidence[0].source_text,
    )

    data = request_data(draft, review, admin, evidence)
    data["evidence"] = (incorrect,) + evidence[1:]

    with pytest.raises(
        ValueError,
        match="25 characters",
    ):
        await service.publish(**data)

    service.ingestion.ingest_document.assert_not_awaited()
    service.db.commit.assert_not_awaited()


async def test_homepage_is_not_enough(
    service, draft, review, admin, evidence
):
    homepage_review = KnowledgeSourceReview(
        document_key=review.document_key,
        source_url="https://bdris.gov.bd/",
        source_name=review.source_name,
        reviewed_at=review.reviewed_at,
        reviewed_flags=review.reviewed_flags,
        evidence_notes=review.evidence_notes,
    )

    data = request_data(
        draft,
        homepage_review,
        admin,
        evidence,
    )

    with pytest.raises(
        ValueError,
        match="homepage",
    ):
        await service.publish(**data)

    service.ingestion.ingest_document.assert_not_awaited()
    service.db.commit.assert_not_awaited()


async def test_audit_contains_reviewer_hash_and_evidence(
    service, draft, review, admin, evidence
):
    await service.publish(
        **request_data(draft, review, admin, evidence)
    )

    service.db.add.assert_called_once()

    audit = service.db.add.call_args.args[0]

    assert isinstance(audit, KnowledgePublicationAudit)
    assert audit.document_key == draft.document_key
    assert audit.reviewer_id == admin.id
    assert audit.source_url == SOURCE_URL
    assert audit.reviewed_at == review.reviewed_at

    expected_hash = hashlib.sha256(
        APPROVED_CONTENT.encode("utf-8")
    ).hexdigest()

    assert audit.approved_content_sha256 == expected_hash
    assert len(audit.claim_evidence) == len(
        draft.review_flags
    )

    assert audit.claim_evidence[0]["review_flag"] == (
        evidence[0].review_flag
    )

    service.db.commit.assert_awaited_once()


async def test_commit_failure_triggers_rollback(
    service, draft, review, admin, evidence
):
    service.db.commit.side_effect = RuntimeError(
        "Database commit failed"
    )

    with pytest.raises(
        RuntimeError,
        match="Database commit failed",
    ):
        await service.publish(
            **request_data(draft, review, admin, evidence)
        )

    service.db.rollback.assert_awaited_once()


async def test_ingestion_failure_triggers_rollback(
    service, draft, review, admin, evidence
):
    service.ingestion.ingest_document.side_effect = (
        RuntimeError("Embedding unavailable")
    )

    with pytest.raises(
        RuntimeError,
        match="Embedding unavailable",
    ):
        await service.publish(
            **request_data(draft, review, admin, evidence)
        )

    service.db.add.assert_not_called()
    service.db.commit.assert_not_awaited()
    service.db.rollback.assert_awaited_once()


async def test_excerpt_missing_from_source_is_rejected(
    service, draft, review, admin, evidence
):
    incorrect = ClaimEvidence(
        review_flag=evidence[0].review_flag,
        source_url=SOURCE_URL,
        source_excerpt=evidence[0].source_excerpt,
        source_text=(
            "A completely unrelated synthetic document "
            "that does not contain the quoted excerpt."
        ),
    )

    data = request_data(draft, review, admin, evidence)
    data["evidence"] = (incorrect,) + evidence[1:]

    with pytest.raises(
        ValueError,
        match="not found",
    ):
        await service.publish(**data)

    service.ingestion.ingest_document.assert_not_awaited()
    service.db.commit.assert_not_awaited()


async def test_short_source_text_is_rejected(
    service, draft, review, admin, evidence
):
    incorrect = ClaimEvidence(
        review_flag=evidence[0].review_flag,
        source_url=SOURCE_URL,
        source_excerpt=evidence[0].source_excerpt,
        source_text="Short",
    )

    data = request_data(draft, review, admin, evidence)
    data["evidence"] = (incorrect,) + evidence[1:]

    with pytest.raises(
        ValueError,
        match="30 characters",
    ):
        await service.publish(**data)

    service.ingestion.ingest_document.assert_not_awaited()
    service.db.commit.assert_not_awaited()


async def test_audit_contains_source_text_hash(
    service, draft, review, admin, evidence
):
    await service.publish(
        **request_data(draft, review, admin, evidence)
    )

    service.db.add.assert_called_once()

    audit = service.db.add.call_args.args[0]

    expected_hash = hashlib.sha256(
        evidence[0].source_text.encode("utf-8")
    ).hexdigest()

    assert (
        audit.claim_evidence[0]["source_text_sha256"]
        == expected_hash
    )

    assert len(expected_hash) == 64
    service.db.commit.assert_awaited_once()
