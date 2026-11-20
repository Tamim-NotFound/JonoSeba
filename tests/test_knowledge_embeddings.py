import math
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import pytest
from app.modules.knowledge.embeddings import (
    EmbeddingError,
    GeminiEmbeddingService,
)
from app.modules.knowledge.models import EMBEDDING_DIMENSIONS


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fake_embedding_client():
    with patch(
        "app.modules.knowledge.embeddings.genai.Client"
    ) as mock_client_class:
        fake_client = mock_client_class.return_value

        fake_client.aio.models.embed_content = AsyncMock()
        fake_client.aio.aclose = AsyncMock()

        yield fake_client


def make_embedding_response(values):
    return SimpleNamespace(
        embeddings=[
            SimpleNamespace(values=values)
        ]
    )


async def test_document_embedding_has_correct_dimensions(
    fake_embedding_client,
):
    fake_embedding_client.aio.models.embed_content.return_value = (
        make_embedding_response(
            [1.0] * EMBEDDING_DIMENSIONS
        )
    )

    service = GeminiEmbeddingService()

    try:
        vector = await service.embed_document(
            "Birth registration service information."
        )
    finally:
        await service.close()

    assert len(vector) == 768

    call_kwargs = (
        fake_embedding_client.aio.models.embed_content
        .await_args.kwargs
    )

    assert call_kwargs["model"] == "gemini-embedding-001"

    assert call_kwargs["config"].task_type == (
        "RETRIEVAL_DOCUMENT"
    )

    assert call_kwargs["config"].output_dimensionality == 768


async def test_query_embedding_uses_retrieval_query(
    fake_embedding_client,
):
    fake_embedding_client.aio.models.embed_content.return_value = (
        make_embedding_response(
            [1.0] * EMBEDDING_DIMENSIONS
        )
    )

    service = GeminiEmbeddingService()

    try:
        vector = await service.embed_query(
            "জন্ম নিবন্ধন কীভাবে করব?"
        )
    finally:
        await service.close()

    assert len(vector) == 768

    call_kwargs = (
        fake_embedding_client.aio.models.embed_content
        .await_args.kwargs
    )

    assert call_kwargs["config"].task_type == (
        "RETRIEVAL_QUERY"
    )


async def test_embedding_is_normalized(
    fake_embedding_client,
):
    fake_embedding_client.aio.models.embed_content.return_value = (
        make_embedding_response(
            [3.0, 4.0]
            + [0.0] * (EMBEDDING_DIMENSIONS - 2)
        )
    )

    service = GeminiEmbeddingService()

    try:
        vector = await service.embed_document(
            "Water supply service."
        )
    finally:
        await service.close()

    magnitude = math.sqrt(
        sum(value * value for value in vector)
    )

    assert magnitude == pytest.approx(1.0)
    assert vector[0] == pytest.approx(0.6)
    assert vector[1] == pytest.approx(0.8)


async def test_empty_text_is_rejected(
    fake_embedding_client,
):
    service = GeminiEmbeddingService()

    try:
        with pytest.raises(ValueError):
            await service.embed_document("   ")
    finally:
        await service.close()

    fake_embedding_client.aio.models.embed_content.assert_not_awaited()


async def test_wrong_dimensions_are_rejected(
    fake_embedding_client,
):
    fake_embedding_client.aio.models.embed_content.return_value = (
        make_embedding_response([1.0, 2.0, 3.0])
    )

    service = GeminiEmbeddingService()

    try:
        with pytest.raises(
            EmbeddingError,
            match="Invalid embedding dimensions",
        ):
            await service.embed_document(
                "Municipal service guide."
            )
    finally:
        await service.close()


async def test_non_finite_values_are_rejected(
    fake_embedding_client,
):
    values = [1.0] * EMBEDDING_DIMENSIONS
    values[0] = float("nan")

    fake_embedding_client.aio.models.embed_content.return_value = (
        make_embedding_response(values)
    )

    service = GeminiEmbeddingService()

    try:
        with pytest.raises(
            EmbeddingError,
            match="non-finite",
        ):
            await service.embed_document(
                "Municipal service guide."
            )
    finally:
        await service.close()


async def test_zero_vector_is_rejected(
    fake_embedding_client,
):
    fake_embedding_client.aio.models.embed_content.return_value = (
        make_embedding_response(
            [0.0] * EMBEDDING_DIMENSIONS
        )
    )

    service = GeminiEmbeddingService()

    try:
        with pytest.raises(
            EmbeddingError,
            match="all zeros",
        ):
            await service.embed_document(
                "Municipal service guide."
            )
    finally:
        await service.close()


async def test_missing_embeddings_are_rejected(
    fake_embedding_client,
):
    fake_embedding_client.aio.models.embed_content.return_value = (
        SimpleNamespace(embeddings=[])
    )

    service = GeminiEmbeddingService()

    try:
        with pytest.raises(
            EmbeddingError,
            match="no embeddings",
        ):
            await service.embed_document(
                "Municipal service guide."
            )
    finally:
        await service.close()
