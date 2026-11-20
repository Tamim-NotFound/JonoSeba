from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.integrations.llm.tool_client import (
    GeminiToolClient,
    knowledge_fallback,
    requires_knowledge_search,
    validate_knowledge_answer,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def source_results():
    return [
        {
            "citation_number": 1,
            "document_title": "Test Service Guide",
            "source_url": "https://service.gov.bd/guide",
            "content": (
                "Synthetic information used for testing."
            ),
        }
    ]


def make_response(
    *,
    text=None,
    function_calls=None,
):
    return SimpleNamespace(
        text=text,
        function_calls=function_calls or [],
        candidates=[],
    )


def make_client(responses):
    client = GeminiToolClient.__new__(
        GeminiToolClient
    )

    client.client = MagicMock()
    client.model = "test-model"

    client.client.aio.models.generate_content = AsyncMock(
        side_effect=responses,
    )

    return client


def test_service_question_requires_search():
    assert requires_knowledge_search(
        "জন্মনিবন্ধনের ফি কত?"
    )

    assert requires_knowledge_search(
        "What documents are required for birth registration?"
    )

    assert requires_knowledge_search(
        "birth registration korte ki ki kagoj lagbe?"
    )


def test_general_message_does_not_require_search():
    assert not requires_knowledge_search("Hello!")

    assert not requires_knowledge_search(
        "আমাদের রাস্তার বাতি নষ্ট।"
    )


def test_valid_citation_has_real_source(
    source_results,
):
    answer = validate_knowledge_answer(
        "Consult the service guide [1].",
        source_results,
    )

    assert answer is not None
    assert "[1]" in answer
    assert "https://service.gov.bd/guide" in answer


def test_invented_citation_is_rejected(
    source_results,
):
    assert validate_knowledge_answer(
        "This rule applies [99].",
        source_results,
    ) is None


def test_missing_citation_is_rejected(
    source_results,
):
    assert validate_knowledge_answer(
        "This rule applies.",
        source_results,
    ) is None


def test_invented_source_url_is_rejected(
    source_results,
):
    assert validate_knowledge_answer(
        (
            "See [1] at "
            "https://unverified.example.com/rule"
        ),
        source_results,
    ) is None


def test_bangla_fallback():
    answer = knowledge_fallback(
        "জন্মনিবন্ধনের ফি কত?"
    )

    assert "পর্যাপ্ত" in answer
    assert "ফি" in answer


def test_banglish_fallback():
    answer = knowledge_fallback(
        "birth registration korte ki ki kagoj lagbe?"
    )

    assert "JonoSeba" in answer
    assert "documents" in answer


async def test_chat_rejects_service_answer_without_search():
    client = make_client(
        [
            make_response(
                text="The official fee is 999 BDT."
            ),
        ]
    )

    answer = await client.generate_response(
        message="জন্মনিবন্ধনের ফি কত?",
        history=None,
        db=MagicMock(),
        current_user=MagicMock(),
    )

    assert "999" not in answer
    assert "পর্যাপ্ত" in answer


async def test_chat_returns_cited_tool_answer(
    source_results,
):
    client = make_client(
        [
            make_response(
                function_calls=[
                    SimpleNamespace(
                        name="search_published_knowledge",
                        args={"query": "birth registration"},
                    )
                ],
            ),
            make_response(
                text="Consult the relevant guide [1]."
            ),
        ]
    )

    tool_result = {
        "success": True,
        "data": {
            "status": "knowledge_found",
            "results": source_results,
        },
    }

    with patch(
        "app.integrations.llm.tool_client.execute_ai_tool",
        new_callable=AsyncMock,
        return_value=tool_result,
    ) as execute_tool:
        answer = await client.generate_response(
            message="What documents are required for birth registration?",
            history=None,
            db=MagicMock(),
            current_user=MagicMock(),
        )

    assert "Consult the relevant guide [1]." in answer
    assert "https://service.gov.bd/guide" in answer
    execute_tool.assert_awaited_once()


async def test_chat_falls_back_when_knowledge_is_empty():
    client = make_client(
        [
            make_response(
                function_calls=[
                    SimpleNamespace(
                        name="search_published_knowledge",
                        args={"query": "birth registration"},
                    )
                ],
            ),
            make_response(
                text="An unsupported fee is 999 BDT."
            ),
        ]
    )

    tool_result = {
        "success": True,
        "data": {
            "status": "no_verified_knowledge_found",
            "results": [],
        },
    }

    with patch(
        "app.integrations.llm.tool_client.execute_ai_tool",
        new_callable=AsyncMock,
        return_value=tool_result,
    ):
        answer = await client.generate_response(
            message="জন্মনিবন্ধনের ফি কত?",
            history=None,
            db=MagicMock(),
            current_user=MagicMock(),
        )

    assert "999" not in answer
    assert "পর্যাপ্ত" in answer


async def test_general_chat_still_works():
    client = make_client(
        [
            make_response(
                text="Hello! How can I help you?"
            ),
        ]
    )

    answer = await client.generate_response(
        message="Hello!",
        history=None,
        db=MagicMock(),
        current_user=MagicMock(),
    )

    assert answer == "Hello! How can I help you?"
