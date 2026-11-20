from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.knowledge.embeddings import GeminiEmbeddingService
from app.modules.knowledge.models import KnowledgeChunk


DEFAULT_SEARCH_LIMIT = 5
MAX_SEARCH_LIMIT = 10

# Cosine distance: 0 = identical direction, 2 = opposite.
# This is a starting threshold, not a calibrated relevance guarantee.
MAX_COSINE_DISTANCE = 0.65


@dataclass(frozen=True)
class KnowledgeSearchResult:
    document_key: str
    document_title: str
    chunk_index: int
    content: str
    language: str
    source_url: str
    source_name: str | None
    verified_at: datetime
    similarity_score: float


class KnowledgeRetrievalService:
    """
    Search published municipal knowledge using pgvector.

    The embedding service converts a citizen question into
    a 768-dimensional query vector.

    PostgreSQL calculates cosine distance and ranks matches.
    """

    def __init__(
        self,
        db: AsyncSession,
        embedding_service: GeminiEmbeddingService,
    ) -> None:
        self.db = db
        self.embedding_service = embedding_service

    async def search(
        self,
        query: str,
        limit: int = DEFAULT_SEARCH_LIMIT,
    ) -> list[KnowledgeSearchResult]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if (
            not isinstance(limit, int)
            or isinstance(limit, bool)
            or not 1 <= limit <= MAX_SEARCH_LIMIT
        ):
            raise ValueError(
                f"Search limit must be between 1 and {MAX_SEARCH_LIMIT}."
            )

        query_vector = await self.embedding_service.embed_query(
            query.strip()
        )

        distance = KnowledgeChunk.embedding.cosine_distance(
            query_vector
        )

        statement = (
            select(
                KnowledgeChunk,
                distance.label("cosine_distance"),
            )
            .where(
                KnowledgeChunk.is_published.is_(True),
                KnowledgeChunk.embedding.is_not(None),
                KnowledgeChunk.source_url.is_not(None),
                KnowledgeChunk.verified_at.is_not(None),
                distance <= MAX_COSINE_DISTANCE,
            )
            .order_by(distance.asc(), KnowledgeChunk.id.asc())
            .limit(limit)
        )

        rows = (await self.db.execute(statement)).all()

        results = []

        for chunk, cosine_distance in rows:
            results.append(
                KnowledgeSearchResult(
                    document_key=chunk.document_key,
                    document_title=chunk.document_title,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    language=chunk.language.value,
                    source_url=chunk.source_url,
                    source_name=chunk.source_name,
                    verified_at=chunk.verified_at,
                    similarity_score=max(
                        0.0,
                        min(1.0, 1.0 - float(cosine_distance)),
                    ),
                )
            )

        return results
