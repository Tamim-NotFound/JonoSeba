from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.knowledge.embeddings import GeminiEmbeddingService
from app.modules.knowledge.master_service_catalog import SERVICE_GUIDES
from app.modules.knowledge.models import KnowledgeChunk


RESEARCH_DOCUMENT_KEYS = tuple(
    f"bd-master-{guide.key}" for guide in SERVICE_GUIDES
)

MAX_RESEARCH_DISTANCE = 0.75


@dataclass(frozen=True)
class ResearchSearchResult:
    document_key: str
    document_title: str
    content: str
    chunk_index: int
    similarity_score: float


class ResearchKnowledgeRetrievalService:
    """
    Search only JonoSeba's saved, unpublished master guides.

    This service does not return official published knowledge
    or arbitrary unpublished database documents.
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
        limit: int = 5,
    ) -> list[ResearchSearchResult]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Research query cannot be empty.")

        if (
            not isinstance(limit, int)
            or isinstance(limit, bool)
            or not 1 <= limit <= 10
        ):
            raise ValueError(
                "Research result limit must be from 1 to 10."
            )

        vector = await self.embedding_service.embed_query(
            query.strip()
        )

        distance = KnowledgeChunk.embedding.cosine_distance(
            vector
        )

        statement = (
            select(
                KnowledgeChunk,
                distance.label("cosine_distance"),
            )
            .where(
                KnowledgeChunk.document_key.in_(
                    RESEARCH_DOCUMENT_KEYS
                ),
                KnowledgeChunk.is_published.is_(False),
                KnowledgeChunk.embedding.is_not(None),
                distance <= MAX_RESEARCH_DISTANCE,
            )
            .order_by(
                distance.asc(),
                KnowledgeChunk.id.asc(),
            )
            .limit(limit)
        )

        rows = (await self.db.execute(statement)).all()

        return [
            ResearchSearchResult(
                document_key=chunk.document_key,
                document_title=chunk.document_title,
                content=chunk.content,
                chunk_index=chunk.chunk_index,
                similarity_score=max(
                    0.0,
                    min(
                        1.0,
                        1.0 - float(cosine_distance),
                    ),
                ),
            )
            for chunk, cosine_distance in rows
        ]
