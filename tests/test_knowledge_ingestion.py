from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.modules.knowledge.ingestion import (
    KnowledgeDocumentInput,
    KnowledgeIngestionService,
)
from app.modules.knowledge.models import KnowledgeLanguage


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fake_db():
    db = MagicMock()
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    return db


@pytest.fixture
def fake_embeddings():
    service = MagicMock()
    service.embed_document = AsyncMock(
        return_value=[0.1] * 768
    )
    return service


def make_document(**overrides):
    values = {
        "document_key": "streetlight-guide",
        "document_title": "Streetlight Service Guide",
        "content": (
            "Citizens can report broken streetlights "
            "through the complaint system."
        ),
        "language": KnowledgeLanguage.ENGLISH,
    }

    values.update(overrides)
    return KnowledgeDocumentInput(**values)


async def test_document_ingestion_saves_chunks(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    result = await service.ingest_document(
        make_document()
    )

    assert result["document_key"] == "streetlight-guide"
    assert result["chunk_count"] == 1
    assert result["is_published"] is False

    fake_db.execute.assert_awaited_once()
    fake_db.add_all.assert_called_once()
    fake_db.commit.assert_awaited_once()
    fake_db.rollback.assert_not_awaited()

    saved_records = fake_db.add_all.call_args.args[0]

    assert len(saved_records) == 1
    assert saved_records[0].embedding == [0.1] * 768
    assert saved_records[0].is_published is False


async def test_bangla_document_is_supported(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    result = await service.ingest_document(
        make_document(
            document_key="bangla-streetlight-guide",
            document_title="সড়কবাতি অভিযোগ নির্দেশিকা",
            content="নষ্ট সড়কবাতির বিষয়ে অভিযোগ জমা দিন।",
            language=KnowledgeLanguage.BANGLA,
        )
    )

    assert result["language"] == "bn"
    assert result["chunk_count"] == 1


async def test_long_document_creates_multiple_chunks(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    result = await service.ingest_document(
        make_document(
            content="Municipal service information. " * 100
        )
    )

    assert result["chunk_count"] > 1
    saved_records = fake_db.add_all.call_args.args[0]
    assert len(saved_records) == result["chunk_count"]

    assert [
        record.chunk_index
        for record in saved_records
    ] == list(range(result["chunk_count"]))

    assert (
        fake_embeddings.embed_document.await_count
        == result["chunk_count"]
    )


async def test_published_document_requires_verification(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    with pytest.raises(
        ValueError,
        match="verified_at",
    ):
        await service.ingest_document(
            make_document(
                is_published=True,
                source_url="https://example.org/guide",
            )
        )

    fake_db.commit.assert_not_awaited()


async def test_published_document_requires_source(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    with pytest.raises(
        ValueError,
        match="source_url",
    ):
        await service.ingest_document(
            make_document(
                is_published=True,
                verified_at=datetime.now(timezone.utc),
            )
        )

    fake_db.commit.assert_not_awaited()


async def test_verified_document_can_be_published(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    result = await service.ingest_document(
        make_document(
            is_published=True,
            verified_at=datetime.now(timezone.utc),
            source_url="https://example.org/guide",
        )
    )

    assert result["is_published"] is True
    saved_records = fake_db.add_all.call_args.args[0]
    assert saved_records[0].is_published is True


async def test_embedding_failure_preserves_existing_data(
    fake_db,
    fake_embeddings,
):
    fake_embeddings.embed_document.side_effect = RuntimeError(
        "Embedding API unavailable"
    )

    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    with pytest.raises(
        RuntimeError,
        match="Embedding API unavailable",
    ):
        await service.ingest_document(
            make_document()
        )

    fake_db.execute.assert_not_awaited()
    fake_db.add_all.assert_not_called()
    fake_db.commit.assert_not_awaited()


async def test_database_failure_triggers_rollback(
    fake_db,
    fake_embeddings,
):
    fake_db.commit.side_effect = RuntimeError(
        "Database commit failed"
    )

    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    with pytest.raises(
        RuntimeError,
        match="Database commit failed",
    ):
        await service.ingest_document(
            make_document()
        )

    fake_db.rollback.assert_awaited_once()


async def test_empty_document_is_rejected(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    with pytest.raises(
        ValueError,
        match="non-empty content",
    ):
        await service.ingest_document(
            make_document(content="   ")
        )

    fake_db.commit.assert_not_awaited()


async def test_reingestion_uses_same_document_key(
    fake_db,
    fake_embeddings,
):
    service = KnowledgeIngestionService(
        db=fake_db,
        embedding_service=fake_embeddings,
    )

    with patch(
        "app.modules.knowledge.ingestion.chunk_document",
        return_value=["First chunk", "Second chunk"],
    ):
        result = await service.ingest_document(
            make_document()
        )

    assert result["chunk_count"] == 2

    records = fake_db.add_all.call_args.args[0]

    assert all(
        record.document_key == "streetlight-guide"
        for record in records
    )

    assert [record.chunk_index for record in records] == [
        0,
        1,
    ]

    # Old document chunks are deleted before the new
    # records are committed.
    assert fake_db.execute.await_count == 1
    fake_db.commit.assert_awaited_once()
