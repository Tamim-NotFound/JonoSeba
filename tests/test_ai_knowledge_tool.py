from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.integrations.llm.tools.knowledge import (
    search_published_knowledge,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fake_dependencies():
    db = MagicMock()

    embedding_service = MagicMock()
    embedding_service.close = AsyncMock()

    retrieval_service = MagicMock()
    retrieval_service.search = AsyncMock(return_value=[])

    with (
        patch(
            "app.integrations.llm.tools.knowledge."
            "GeminiEmbeddingService",
            return_value=embedding_service,
        ),
        patch(
            "app.integrations.llm.tools.knowledge."
            "KnowledgeRetrievalService",
            return_value=retrieval_service,
        ),
    ):
        yield db, embedding_service, retrieval_service


async def test_returns_source_linked_knowledge(
    fake_dependencies,
):
    db, embedding_service, retrieval_service = (
        fake_dependencies
    )

    verified_at = datetime.now(timezone.utc)

    retrieval_service.search.return_value = [
        SimpleNamespace(
            document_title="Streetlight Guide",
            content="Report a broken streetlight.",
            language="en",
            source_url="https://example.org/test-only",
            source_name="Test Source",
            verified_at=verified_at,
            similarity_score=0.9,
        )
    ]

    result = await search_published_knowledge(
        db,
        "How can I report a broken streetlight?",
    )

    assert result["status"] == "knowledge_found"
    assert len(result["results"]) == 1

    item = result["results"][0]

    assert item["citation_number"] == 1
    assert item["document_title"] == "Streetlight Guide"
    assert item["source_url"] == (
        "https://example.org/test-only"
    )
    assert item["verified_at"] == verified_at.isoformat()

    retrieval_service.search.assert_awaited_once_with(
        query="How can I report a broken streetlight?",
        limit=5,
    )

    embedding_service.close.assert_awaited_once()


async def test_no_knowledge_returns_safe_fallback(
    fake_dependencies,
):
    db, embedding_service, retrieval_service = (
        fake_dependencies
    )

    result = await search_published_knowledge(
        db,
        "Unknown municipal procedure",
    )

    assert result["status"] == (
        "no_verified_knowledge_found"
    )
    assert result["results"] == []
    assert "Do not invent" in result["message"]

    embedding_service.close.assert_awaited_once()


async def test_bangla_query_is_supported(
    fake_dependencies,
):
    db, _, retrieval_service = fake_dependencies

    await search_published_knowledge(
        db,
        "রাস্তার বাতি নষ্ট হলে কী করব?",
    )

    retrieval_service.search.assert_awaited_once_with(
        query="রাস্তার বাতি নষ্ট হলে কী করব?",
        limit=5,
    )


async def test_empty_query_is_rejected(
    fake_dependencies,
):
    db, embedding_service, retrieval_service = (
        fake_dependencies
    )

    with pytest.raises(ValueError):
        await search_published_knowledge(db, "   ")

    retrieval_service.search.assert_not_awaited()
    embedding_service.close.assert_not_awaited()


async def test_embedding_client_closes_on_error(
    fake_dependencies,
):
    db, embedding_service, retrieval_service = (
        fake_dependencies
    )

    retrieval_service.search.side_effect = RuntimeError(
        "Database unavailable"
    )

    with pytest.raises(
        RuntimeError,
        match="Database unavailable",
    ):
        await search_published_knowledge(
            db,
            "Water supply",
        )

    embedding_service.close.assert_awaited_once()


async def test_long_excerpts_are_truncated(
    fake_dependencies,
):
    db, _, retrieval_service = fake_dependencies

    retrieval_service.search.return_value = [
        SimpleNamespace(
            document_title="Long Guide",
            content="A" * 3000,
            language="en",
            source_url="https://example.org/test-only",
            source_name="Test Source",
            verified_at=datetime.now(timezone.utc),
            similarity_score=0.9,
        )
    ]

    result = await search_published_knowledge(
        db,
        "Long document question",
    )

    assert len(result["results"][0]["content"]) == 1500


async def test_too_long_query_is_rejected(
    fake_dependencies,
):
    db, embedding_service, retrieval_service = (
        fake_dependencies
    )

    with pytest.raises(ValueError):
        await search_published_knowledge(
            db,
            "A" * 2001,
        )

    retrieval_service.search.assert_not_awaited()
    embedding_service.close.assert_not_awaited()
