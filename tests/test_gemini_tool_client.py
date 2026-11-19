from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import pytest
from google.genai import types
from app.integrations.llm.tool_client import GeminiToolClient

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def citizen():
    return SimpleNamespace(
        id=2,
        is_active=True,
    )


@pytest.fixture
def fake_db():
    return SimpleNamespace()


def make_tool_call_response(
    tool_name: str,
    arguments: dict,
):
    function_call_part = types.Part.from_function_call(
        name=tool_name,
        args=arguments,
    )

    model_content = types.Content(
        role="model",
        parts=[function_call_part],
    )

    return SimpleNamespace(
        function_calls=[
            SimpleNamespace(
                name=tool_name,
                args=arguments,
            )
        ],
        candidates=[
            SimpleNamespace(
                content=model_content,
            )
        ],
        text=None,
    )


def make_final_response(text: str):
    return SimpleNamespace(
        function_calls=[],
        candidates=[],
        text=text,
    )


async def test_gemini_executes_department_tool_and_returns_answer(
    citizen,
    fake_db,
):
    tool_response = make_tool_call_response(
        "list_departments",
        {"search": "Water"},
    )

    final_response = make_final_response(
        "The Water Supply department is active."
    )

    fake_generate = AsyncMock(
        side_effect=[
            tool_response,
            final_response,
        ]
    )

    fake_execute = AsyncMock(
        return_value={
            "success": True,
            "data": {
                "departments": [
                    {
                        "id": 1,
                        "name": "Water Supply",
                        "description": "Water services",
                    }
                ],
                "count": 1,
            },
        }
    )

    with (
        patch(
            "app.integrations.llm.tool_client."
            "execute_ai_tool",
            fake_execute,
        ),
        patch(
            "app.integrations.llm.tool_client."
            "genai.Client",
        ) as mock_client_class,
    ):
        fake_client = mock_client_class.return_value

        fake_client.aio.models.generate_content = (
            fake_generate
        )
        fake_client.aio.aclose = AsyncMock()

        client = GeminiToolClient()

        try:
            answer = await client.generate_response(
                message="Which water department is available?",
                history=[],
                db=fake_db,
                current_user=citizen,
            )
        finally:
            await client.close()

    assert answer == (
        "The Water Supply department is active."
    )

    assert fake_generate.await_count == 2

    fake_execute.assert_awaited_once_with(
        tool_name="list_departments",
        arguments={"search": "Water"},
        db=fake_db,
        current_user=citizen,
    )

    second_request = fake_generate.await_args_list[1]
    contents = second_request.kwargs["contents"]
    tool_result_content = contents[-1]
    assert tool_result_content.parts is not None

    function_response = (
        tool_result_content.parts[0].function_response
    )

    assert function_response is not None
    assert function_response.name == "list_departments"

    assert function_response.response["success"] is True


async def test_gemini_passes_authenticated_user_to_complaint_tool(
    citizen,
    fake_db,
):
    tool_response = make_tool_call_response(
        "get_my_complaint_status",
        {"complaint_id": 15},
    )

    final_response = make_final_response(
        "Your complaint 15 is pending."
    )

    fake_generate = AsyncMock(
        side_effect=[
            tool_response,
            final_response,
        ]
    )

    fake_execute = AsyncMock(
        return_value={
            "success": True,
            "data": {
                "found": True,
                "complaint": {
                    "id": 15,
                    "status": "pending",
                },
            },
        }
    )

    with (
        patch(
            "app.integrations.llm.tool_client."
            "execute_ai_tool",
            fake_execute,
        ),
        patch(
            "app.integrations.llm.tool_client."
            "genai.Client",
        ) as mock_client_class,
    ):
        fake_client = mock_client_class.return_value

        fake_client.aio.models.generate_content = (
            fake_generate
        )
        fake_client.aio.aclose = AsyncMock()

        client = GeminiToolClient()

        try:
            answer = await client.generate_response(
                message="Check complaint 15",
                history=[],
                db=fake_db,
                current_user=citizen,
            )
        finally:
            await client.close()

    assert answer == "Your complaint 15 is pending."

    fake_execute.assert_awaited_once_with(
        tool_name="get_my_complaint_status",
        arguments={"complaint_id": 15},
        db=fake_db,
        current_user=citizen,
    )


async def test_gemini_can_reply_without_tool_call(
    citizen,
    fake_db,
):
    fake_generate = AsyncMock(
        return_value=make_final_response(
            "Hello! How can I help you?"
        )
    )

    fake_execute = AsyncMock()

    with (
        patch(
            "app.integrations.llm.tool_client."
            "execute_ai_tool",
            fake_execute,
        ),
        patch(
            "app.integrations.llm.tool_client."
            "genai.Client",
        ) as mock_client_class,
    ):
        fake_client = mock_client_class.return_value

        fake_client.aio.models.generate_content = (
            fake_generate
        )
        fake_client.aio.aclose = AsyncMock()

        client = GeminiToolClient()

        try:
            answer = await client.generate_response(
                message="Hello",
                history=[],
                db=fake_db,
                current_user=citizen,
            )
        finally:
            await client.close()

    assert answer == "Hello! How can I help you?"
    assert fake_generate.await_count == 1
    fake_execute.assert_not_awaited()
