from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import pytest
from app.modules.knowledge.answering import (
    KnowledgeAnswerService,
)
from app.modules.knowledge.retrieval import (
    KnowledgeSearchResult,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


def make_match(index=0):
    return KnowledgeSearchResult(
        document_key="streetlight-guide",
        document_title="Streetlight Service Guide",
        chunk_index=index,
        content="Report a broken streetlight to the service desk.",
        language="en",
        source_url="https://example.org/test-only",
        source_name="Test Fixture",
        verified_at=datetime.now(timezone.utc),
        similarity_score=0.9,
    )


def build_service(matches, response_text="Answer [1]"):
    retrieval = MagicMock()
    retrieval.search = AsyncMock(return_value=matches)

    client = MagicMock()
    client.aio.models.generate_content = AsyncMock(
        return_value=SimpleNamespace(text=response_text)
    )

    service = KnowledgeAnswerService(
        retrieval_service=retrieval,
        client=client,
    )

    return service, retrieval, client


async def test_grounded_answer_has_source():
    service, retrieval, client = build_service(
        [make_match()],
        "Report the problem to the service desk [1].",
    )

    result = await service.answer_question(
        "How do I report a broken streetlight?"
    )

    assert result.grounded is True
    assert "[1]" in result.answer
    assert len(result.sources) == 1
    assert result.sources[0].citation_number == 1

    retrieval.search.assert_awaited_once()
    client.aio.models.generate_content.assert_awaited_once()


async def test_no_matches_returns_fallback_without_gemini():
    service, _, client = build_service([])

    result = await service.answer_question(
        "Unknown municipal procedure"
    )

    assert result.grounded is False
    assert result.sources == ()
    assert "enough reliable information" in result.answer

    client.aio.models.generate_content.assert_not_awaited()


async def test_bangla_fallback():
    service, _, client = build_service([])

    result = await service.answer_question(
        "এই সেবার নিয়ম কী?"
    )

    assert result.grounded is False
    assert "পর্যাপ্ত নির্ভরযোগ্য তথ্য" in result.answer

    client.aio.models.generate_content.assert_not_awaited()


async def test_answer_without_citation_is_rejected():
    service, _, _ = build_service(
        [make_match()],
        "Here is a procedure without any citation.",
    )

    result = await service.answer_question(
        "What is the procedure?"
    )

    assert result.grounded is False
    assert result.sources == ()


async def test_invented_citation_is_rejected():
    service, _, _ = build_service(
        [make_match()],
        "Follow the procedure [99].",
    )

    result = await service.answer_question(
        "What is the procedure?"
    )

    assert result.grounded is False
    assert result.sources == ()


async def test_only_cited_sources_are_returned():
    service, _, _ = build_service(
        [make_match(0), make_match(1)],
        "The relevant information is in excerpt [2].",
    )

    result = await service.answer_question(
        "Which guide is relevant?"
    )

    assert result.grounded is True
    assert len(result.sources) == 1
    assert result.sources[0].citation_number == 2


async def test_empty_question_is_rejected():
    service, retrieval, client = build_service(
        [make_match()]
    )

    with pytest.raises(ValueError):
        await service.answer_question("   ")

    retrieval.search.assert_not_awaited()
    client.aio.models.generate_content.assert_not_awaited()


async def test_question_is_included_in_gemini_context():
    service, _, client = build_service(
        [make_match()],
        "Information [1]",
    )

    await service.answer_question(
        "  রাস্তার বাতি নষ্ট হলে কী করব?  "
    )

    call = client.aio.models.generate_content.await_args

    assert "রাস্তার বাতি নষ্ট হলে কী করব?" in (
        call.kwargs["contents"]
    )
    assert "Streetlight Service Guide" in (
        call.kwargs["contents"]
    )
