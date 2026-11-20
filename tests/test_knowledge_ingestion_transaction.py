from app.modules.knowledge.models import KnowledgeLanguage
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.modules.knowledge.ingestion import (
    KnowledgeDocumentInput,
    KnowledgeIngestionService,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def document():
    return KnowledgeDocumentInput(
        document_key="transaction-test",
        document_title="Transaction Test Guide",
        content=(
            "This is a test document with enough "
            "content for the ingestion transaction."
        ),
        language=KnowledgeLanguage.ENGLISH,
        source_url="https://example.org/test-only",
        source_name="Test Fixture",
        verified_at=datetime.now(timezone.utc),
        is_published=False,
    )


@pytest.fixture
def dependencies():
    db = MagicMock()

    db.execute = AsyncMock()
    db.flush = AsyncMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()

    embeddings = MagicMock()
    embeddings.embed_document = AsyncMock(
        return_value=[1.0] + [0.0] * 767
    )

    return db, embeddings


async def test_commit_false_flushes_without_committing(
    document, dependencies
):
    db, embeddings = dependencies

    service = KnowledgeIngestionService(
        db=db,
        embedding_service=embeddings,
    )

    with patch(
        "app.modules.knowledge.ingestion.chunk_document",
        return_value=["Test chunk"],
    ):
        result = await service.ingest_document(
            document,
            commit=False,
        )

    assert result["chunk_count"] == 1

    db.execute.assert_awaited_once()
    db.add_all.assert_called_once()
    db.flush.assert_awaited_once()

    db.commit.assert_not_awaited()
    db.rollback.assert_not_awaited()


async def test_default_ingestion_still_commits(
    document, dependencies
):
    db, embeddings = dependencies

    service = KnowledgeIngestionService(
        db=db,
        embedding_service=embeddings,
    )

    with patch(
        "app.modules.knowledge.ingestion.chunk_document",
        return_value=["Test chunk"],
    ):
        await service.ingest_document(document)

    db.commit.assert_awaited_once()
    db.flush.assert_not_awaited()


async def test_flush_failure_rolls_back(
    document, dependencies
):
    db, embeddings = dependencies

    db.flush.side_effect = RuntimeError(
        "Database flush failed"
    )

    service = KnowledgeIngestionService(
        db=db,
        embedding_service=embeddings,
    )

    with patch(
        "app.modules.knowledge.ingestion.chunk_document",
        return_value=["Test chunk"],
    ):
        with pytest.raises(
            RuntimeError,
            match="Database flush failed",
        ):
            await service.ingest_document(
                document,
                commit=False,
            )

    db.commit.assert_not_awaited()
    db.rollback.assert_awaited_once()
