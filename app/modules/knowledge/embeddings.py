import math
from google import genai
from google.genai import types
from app.core.config import settings
from app.modules.knowledge.models import EMBEDDING_DIMENSIONS


EMBEDDING_MODEL = "gemini-embedding-001"


class EmbeddingError(Exception):
    """Raised when embedding generation or validation fails."""


class GeminiEmbeddingService:
    """
    Generate multilingual text embeddings using Gemini.

    All returned vectors must match the knowledge_chunks
    database column: VECTOR(768).
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

    async def embed_document(self, text: str) -> list[float]:
        """
        Generate an embedding for a knowledge document chunk.
        """

        return await self._embed(
            text=text,
            task_type="RETRIEVAL_DOCUMENT",
        )

    async def embed_query(self, text: str) -> list[float]:
        """
        Generate an embedding for a citizen search query.
        """

        return await self._embed(
            text=text,
            task_type="RETRIEVAL_QUERY",
        )

    async def _embed(
        self,
        *,
        text: str,
        task_type: str,
    ) -> list[float]:
        if not isinstance(text, str):
            raise ValueError("Embedding text must be a string.")

        text = text.strip()

        if not text:
            raise ValueError("Embedding text cannot be empty.")

        response = await self.client.aio.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=EMBEDDING_DIMENSIONS,
            ),
        )

        if not response.embeddings:
            raise EmbeddingError(
                "Embedding API returned no embeddings."
            )

        values = response.embeddings[0].values

        if values is None:
            raise EmbeddingError(
                "Embedding API returned no vector values."
            )

        vector = [float(value) for value in values]

        if len(vector) != EMBEDDING_DIMENSIONS:
            raise EmbeddingError(
                "Invalid embedding dimensions: "
                f"expected {EMBEDDING_DIMENSIONS}, "
                f"received {len(vector)}."
            )

        if not all(math.isfinite(value) for value in vector):
            raise EmbeddingError(
                "Embedding contains non-finite values."
            )

        if not any(value != 0.0 for value in vector):
            raise EmbeddingError(
                "Embedding vector cannot be all zeros."
            )

        # Normalize to unit length for consistent
        # cosine-similarity calculations.
        magnitude = math.sqrt(
            sum(value * value for value in vector)
        )

        if not math.isfinite(magnitude) or magnitude == 0.0:
            raise EmbeddingError(
                "Embedding magnitude is invalid."
            )

        return [
            value / magnitude
            for value in vector
        ]

    async def close(self) -> None:
        """Close the Gemini async HTTP client."""

        await self.client.aio.aclose()
