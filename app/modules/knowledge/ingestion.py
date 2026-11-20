from dataclasses import dataclass
from datetime import datetime, timezone
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.knowledge.chunking import chunk_document
from app.modules.knowledge.embeddings import GeminiEmbeddingService
from app.modules.knowledge.models import (
    KnowledgeChunk,
    KnowledgeLanguage,
)


@dataclass(frozen=True)
class KnowledgeDocumentInput:
    document_key: str
    document_title: str
    content: str
    language: KnowledgeLanguage
    source_url: str | None = None
    source_name: str | None = None
    verified_at: datetime | None = None
    is_published: bool = False


class KnowledgeIngestionService:
    """
    Ingest a municipal service document into PostgreSQL.

    Embeddings are generated before database changes.

    Existing chunks are replaced within one transaction.
    """

    def __init__(
        self,
        db: AsyncSession,
        embedding_service: GeminiEmbeddingService,
    ) -> None:
        self.db = db
        self.embedding_service = embedding_service

    async def ingest_document(
        self,
        document: KnowledgeDocumentInput,
    ) -> dict:
        self._validate_document(document)

        chunks = chunk_document(document.content)

        if not chunks:
            raise ValueError(
                "Document must contain non-empty content."
            )

        # Generate every embedding before modifying the DB.
        # An API failure must not delete existing knowledge.
        embeddings = []

        for chunk in chunks:
            vector = await self.embedding_service.embed_document(
                chunk
            )
            embeddings.append(vector)

        records = [
            KnowledgeChunk(
                document_key=document.document_key.strip(),
                document_title=document.document_title.strip(),
                chunk_index=index,
                content=chunk,
                language=document.language,
                source_url=document.source_url,
                source_name=document.source_name,
                verified_at=document.verified_at,
                is_published=document.is_published,
                embedding=embeddings[index],
            )
            for index, chunk in enumerate(chunks)
        ]

        try:
            # Delete and insert participate in the same
            # database transaction.
            await self.db.execute(
                delete(KnowledgeChunk).where(
                    KnowledgeChunk.document_key
                    == document.document_key.strip()
                )
            )

            self.db.add_all(records)

            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

        return {
            "document_key": document.document_key.strip(),
            "chunk_count": len(records),
            "language": document.language.value,
            "is_published": document.is_published,
        }

    @staticmethod
    def _validate_document(
        document: KnowledgeDocumentInput,
    ) -> None:
        if not document.document_key.strip():
            raise ValueError(
                "document_key cannot be empty."
            )

        if len(document.document_key) > 150:
            raise ValueError(
                "document_key cannot exceed 150 characters."
            )

        if not document.document_title.strip():
            raise ValueError(
                "document_title cannot be empty."
            )

        if len(document.document_title) > 255:
            raise ValueError(
                "document_title cannot exceed 255 characters."
            )

        if not isinstance(
            document.language,
            KnowledgeLanguage,
        ):
            raise ValueError(
                "Unsupported knowledge language."
            )

        if (
            document.source_url is not None
            and len(document.source_url) > 2048
        ):
            raise ValueError(
                "source_url cannot exceed 2048 characters."
            )

        if (
            document.source_name is not None
            and len(document.source_name) > 255
        ):
            raise ValueError(
                "source_name cannot exceed 255 characters."
            )

        if document.verified_at is not None:
            if (
                document.verified_at.tzinfo is None
                or document.verified_at.utcoffset() is None
            ):
                raise ValueError(
                    "verified_at must include a timezone."
                )

            if document.verified_at > datetime.now(timezone.utc):
                raise ValueError(
                    "verified_at cannot be in the future."
                )

        # A published document must have verification metadata.
        # This validates metadata presence, not source authenticity.
        if document.is_published:
            if document.verified_at is None:
                raise ValueError(
                    "Published documents require verified_at."
                )

            if not document.source_url:
                raise ValueError(
                    "Published documents require source_url."
                )

            if not document.source_url.startswith(
                ("https://", "http://")
            ):
                raise ValueError(
                    "Published source_url must be an HTTP(S) URL."
                )
