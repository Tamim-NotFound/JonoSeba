import uuid
from unittest.mock import AsyncMock
import pytest
from sqlalchemy import delete, select
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.modules.knowledge.ingestion import (
    KnowledgeDocumentInput,
    KnowledgeIngestionService,
)
from app.modules.knowledge.models import (
    KnowledgeChunk,
    KnowledgeLanguage,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def db_session():
    production_url = make_url(settings.DATABASE_URL)

    test_url = production_url.set(
        database="jonoseba_test_db"
    )

    if test_url.database == production_url.database:
        raise RuntimeError(
            "Integration tests must not use production DB."
        )

    engine = create_async_engine(test_url)

    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def fake_embeddings():
    service = AsyncMock()

    service.embed_document.return_value = (
        [1.0] + [0.0] * 767
    )

    return service


@pytest.fixture
def document_key():
    return f"integration-test-{uuid.uuid4().hex}"


async def cleanup_document(
    db: AsyncSession,
    key: str,
):
    await db.execute(
        delete(KnowledgeChunk).where(
            KnowledgeChunk.document_key == key
        )
    )

    await db.commit()


async def test_real_postgres_ingestion(
    db_session,
    fake_embeddings,
    document_key,
):
    service = KnowledgeIngestionService(
        db=db_session,
        embedding_service=fake_embeddings,
    )

    try:
        result = await service.ingest_document(
            KnowledgeDocumentInput(
                document_key=document_key,
                document_title="Integration Test Guide",
                content="Streetlight complaints can be submitted.",
                language=KnowledgeLanguage.ENGLISH,
            )
        )

        assert result["chunk_count"] == 1

        rows = (
            await db_session.execute(
                select(KnowledgeChunk).where(
                    KnowledgeChunk.document_key
                    == document_key
                )
            )
        ).scalars().all()

        assert len(rows) == 1
        assert rows[0].content == (
            "Streetlight complaints can be submitted."
        )
        assert rows[0].is_published is False
        assert len(rows[0].embedding) == 768

    finally:
        await cleanup_document(
            db_session,
            document_key,
        )


async def test_real_postgres_reingestion_replaces_chunks(
    db_session,
    fake_embeddings,
    document_key,
):
    service = KnowledgeIngestionService(
        db=db_session,
        embedding_service=fake_embeddings,
    )

    try:
        await service.ingest_document(
            KnowledgeDocumentInput(
                document_key=document_key,
                document_title="Old Guide",
                content="Old service information.",
                language=KnowledgeLanguage.ENGLISH,
            )
        )

        await service.ingest_document(
            KnowledgeDocumentInput(
                document_key=document_key,
                document_title="Updated Guide",
                content="Updated service information.",
                language=KnowledgeLanguage.ENGLISH,
            )
        )

        rows = (
            await db_session.execute(
                select(KnowledgeChunk).where(
                    KnowledgeChunk.document_key
                    == document_key
                )
            )
        ).scalars().all()

        assert len(rows) == 1
        assert rows[0].document_title == "Updated Guide"
        assert rows[0].content == (
            "Updated service information."
        )

    finally:
        await cleanup_document(
            db_session,
            document_key,
        )


async def test_embedding_failure_preserves_real_data(
    db_session,
    fake_embeddings,
    document_key,
):
    service = KnowledgeIngestionService(
        db=db_session,
        embedding_service=fake_embeddings,
    )

    try:
        await service.ingest_document(
            KnowledgeDocumentInput(
                document_key=document_key,
                document_title="Existing Guide",
                content="Existing verified information.",
                language=KnowledgeLanguage.ENGLISH,
            )
        )

        fake_embeddings.embed_document.side_effect = (
            RuntimeError("Embedding API failed")
        )

        with pytest.raises(
            RuntimeError,
            match="Embedding API failed",
        ):
            await service.ingest_document(
                KnowledgeDocumentInput(
                    document_key=document_key,
                    document_title="Broken Update",
                    content="New information.",
                    language=KnowledgeLanguage.ENGLISH,
                )
            )

        rows = (
            await db_session.execute(
                select(KnowledgeChunk).where(
                    KnowledgeChunk.document_key
                    == document_key
                )
            )
        ).scalars().all()

        assert len(rows) == 1
        assert rows[0].document_title == "Existing Guide"

    finally:
        await cleanup_document(
            db_session,
            document_key,
        )