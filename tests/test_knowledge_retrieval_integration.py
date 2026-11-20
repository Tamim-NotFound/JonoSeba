import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock
import pytest
from sqlalchemy import delete
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.modules.knowledge.models import (
    KnowledgeChunk,
    KnowledgeLanguage,
)
from app.modules.knowledge.retrieval import (
    KnowledgeRetrievalService,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


# Simple unit-length vectors for deterministic tests.
VECTOR_A = [1.0, 0.0] + [0.0] * 766
VECTOR_B = [0.8, 0.6] + [0.0] * 766
VECTOR_OPPOSITE = [-1.0, 0.0] + [0.0] * 766


@pytest.fixture
async def db_session():
    production_url = make_url(settings.DATABASE_URL)

    if production_url.database != "jonoseba_db":
        raise RuntimeError(
            "Unexpected configured database. "
            "Review test database settings before proceeding."
        )

    test_url = production_url.set(
        database="jonoseba_test_db"
    )

    engine = create_async_engine(test_url)

    factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    try:
        async with factory() as session:
            yield session
    finally:
        await engine.dispose()


@pytest.fixture
def fake_embeddings():
    service = AsyncMock()
    service.embed_query.return_value = VECTOR_A
    return service


@pytest.fixture
def test_document_key():
    return f"retrieval-test-{uuid.uuid4().hex}"


def make_chunk(
    key,
    index,
    *,
    vector=VECTOR_A,
    published=True,
    source_url="https://example.org/test-only",
    verified_at=None,
    language=KnowledgeLanguage.ENGLISH,
):
    if verified_at is None:
        verified_at = datetime.now(timezone.utc)

    return KnowledgeChunk(
        document_key=key,
        document_title="Integration Test Guide",
        chunk_index=index,
        content=f"Test knowledge chunk {index}",
        language=language,
        source_url=source_url,
        source_name="Automated Test Fixture",
        verified_at=verified_at,
        is_published=published,
        embedding=vector,
    )


async def run_search_with_chunks(
    db_session,
    fake_embeddings,
    key,
    chunks,
):
    try:
        db_session.add_all(chunks)
        await db_session.commit()

        service = KnowledgeRetrievalService(
            db=db_session,
            embedding_service=fake_embeddings,
        )

        return await service.search(
            "Test municipal service question",
            limit=10,
        )

    finally:
        await db_session.rollback()

        await db_session.execute(
            delete(KnowledgeChunk).where(
                KnowledgeChunk.document_key == key
            )
        )

        await db_session.commit()


async def test_real_postgres_similarity_ranking(
    db_session,
    fake_embeddings,
    test_document_key,
):
    results = await run_search_with_chunks(
        db_session,
        fake_embeddings,
        test_document_key,
        [
            make_chunk(
                test_document_key,
                0,
                vector=VECTOR_B,
            ),
            make_chunk(
                test_document_key,
                1,
                vector=VECTOR_A,
            ),
        ],
    )

    matching = [
        result
        for result in results
        if result.document_key == test_document_key
    ]

    assert len(matching) == 2
    assert matching[0].chunk_index == 1
    assert matching[1].chunk_index == 0
    assert matching[0].similarity_score > (
        matching[1].similarity_score
    )


async def test_unpublished_chunks_are_excluded(
    db_session,
    fake_embeddings,
    test_document_key,
):
    results = await run_search_with_chunks(
        db_session,
        fake_embeddings,
        test_document_key,
        [
            make_chunk(
                test_document_key,
                0,
                published=False,
            ),
        ],
    )

    assert not any(
        result.document_key == test_document_key
        for result in results
    )


async def test_missing_source_is_excluded(
    db_session,
    fake_embeddings,
    test_document_key,
):
    results = await run_search_with_chunks(
        db_session,
        fake_embeddings,
        test_document_key,
        [
            make_chunk(
                test_document_key,
                0,
                source_url=None,
            ),
        ],
    )

    assert not any(
        result.document_key == test_document_key
        for result in results
    )


async def test_bangla_chunk_is_retrievable(
    db_session,
    fake_embeddings,
    test_document_key,
):
    results = await run_search_with_chunks(
        db_session,
        fake_embeddings,
        test_document_key,
        [
            make_chunk(
                test_document_key,
                0,
                language=KnowledgeLanguage.BANGLA,
            ),
        ],
    )

    matching = [
        result
        for result in results
        if result.document_key == test_document_key
    ]

    assert len(matching) == 1
    assert matching[0].language == "bn"
    assert matching[0].source_name == (
        "Automated Test Fixture"
    )


async def test_irrelevant_vectors_are_excluded(
    db_session,
    fake_embeddings,
    test_document_key,
):
    results = await run_search_with_chunks(
        db_session,
        fake_embeddings,
        test_document_key,
        [
            make_chunk(
                test_document_key,
                0,
                vector=VECTOR_OPPOSITE,
            ),
        ],
    )

    assert not any(
        result.document_key == test_document_key
        for result in results
    )
