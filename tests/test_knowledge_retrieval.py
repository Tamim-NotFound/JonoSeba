from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import pytest
from app.modules.knowledge.models import KnowledgeLanguage
from app.modules.knowledge.retrieval import (
    KnowledgeRetrievalService,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fake_db():
    db = MagicMock()

    # AsyncSession.execute() is asynchronous.
    db.execute = AsyncMock()

    # SQLAlchemy Result.all() is synchronous.
    result = MagicMock()
    result.all.return_value = []

    db.execute.return_value = result

    return db


@pytest.fixture
def fake_embeddings():
    service = MagicMock()
    service.embed_query = AsyncMock(
        return_value=[1.0] + [0.0] * 767
    )
    return service


def make_chunk(**overrides):
    values = {
        "document_key": "streetlight-guide",
        "document_title": "Streetlight Service Guide",
        "chunk_index": 0,
        "content": "Report damaged streetlights.",
        "language": KnowledgeLanguage.ENGLISH,
        "source_url": "https://example.org/guide",
        "source_name": "Municipal Authority",
        "verified_at": datetime.now(timezone.utc),
    }

    values.update(overrides)
    return SimpleNamespace(**values)


async def test_search_returns_ranked_results(
    fake_db,
    fake_embeddings,
):
    fake_db.execute.return_value.all.return_value = [
        (make_chunk(chunk_index=0), 0.1),
        (make_chunk(chunk_index=1), 0.3),
    ]

    service = KnowledgeRetrievalService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    results = await service.search(
        "Where can I report broken streetlights?"
    )

    assert len(results) == 2
    assert results[0].similarity_score == pytest.approx(0.9)
    assert results[1].similarity_score == pytest.approx(0.7)

    fake_embeddings.embed_query.assert_awaited_once()
    fake_db.execute.assert_awaited_once()


async def test_bangla_query_is_supported(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeRetrievalService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    results = await service.search(
        "রাস্তার বাতি নষ্ট হলে কী করব?"
    )

    assert results == []

    fake_embeddings.embed_query.assert_awaited_once_with(
        "রাস্তার বাতি নষ্ট হলে কী করব?"
    )


async def test_empty_query_is_rejected(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeRetrievalService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    with pytest.raises(ValueError):
        await service.search("   ")

    fake_db.execute.assert_not_awaited()
    fake_embeddings.embed_query.assert_not_awaited()


@pytest.mark.parametrize("limit", [0, -1, 11, True, 1.5])
async def test_invalid_limit_is_rejected(
    fake_db,
    fake_embeddings,
    limit,
):
    service = KnowledgeRetrievalService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    with pytest.raises(ValueError):
        await service.search("Streetlight complaint", limit=limit)

    fake_db.execute.assert_not_awaited()


async def test_custom_limit_is_applied(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeRetrievalService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    await service.search("Water supply", limit=3)
    statement = fake_db.execute.await_args.args[0]
    compiled = statement.compile()
    assert 3 in compiled.params.values()


async def test_results_include_source_metadata(
    fake_db,
    fake_embeddings,
):
    verified_at = datetime.now(timezone.utc)

    fake_db.execute.return_value.all.return_value = [
        (
            make_chunk(
                language=KnowledgeLanguage.BANGLA,
                source_url="https://example.org/bn",
                verified_at=verified_at,
            ),
            0.2,
        )
    ]

    service = KnowledgeRetrievalService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    results = await service.search("সেবা সংক্রান্ত তথ্য")

    assert results[0].language == "bn"
    assert results[0].source_url == "https://example.org/bn"
    assert results[0].verified_at == verified_at
    assert results[0].similarity_score == pytest.approx(0.8)


async def test_query_is_trimmed(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeRetrievalService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    await service.search("  Water supply complaint  ")

    fake_embeddings.embed_query.assert_awaited_once_with(
        "Water supply complaint"
    )
