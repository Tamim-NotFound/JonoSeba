from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.integrations.llm.tool_client import (
    JONOSEBA_TOOL_SYSTEM_PROMPT,
)
from app.integrations.llm.tools.declarations import (
    JONOSEBA_GEMINI_TOOLS,
)
from app.integrations.llm.tools.executor import (
    execute_ai_tool,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def dependencies():
    return MagicMock(), MagicMock()


async def test_all_three_tools_are_registered():
    declarations = (
        JONOSEBA_GEMINI_TOOLS[0].function_declarations
    )

    names = {
        declaration.name
        for declaration in declarations
    }

    assert names == {
        "list_departments",
        "get_my_complaint_status",
        "search_published_knowledge",
    }


async def test_rag_instructions_preserve_original_prompt():
    assert "search_published_knowledge" in (
        JONOSEBA_TOOL_SYSTEM_PROMPT
    )
    assert "Do not invent fees" in (
        JONOSEBA_TOOL_SYSTEM_PROMPT
    )


async def test_valid_knowledge_search_is_dispatched(
    dependencies,
):
    db, current_user = dependencies

    expected = {
        "status": "knowledge_found",
        "results": [],
    }

    with patch(
        "app.integrations.llm.tools.executor."
        "search_published_knowledge",
        new_callable=AsyncMock,
    ) as knowledge_tool:
        knowledge_tool.return_value = expected

        result = await execute_ai_tool(
            tool_name="search_published_knowledge",
            arguments={
                "query": "  রাস্তার বাতি নষ্ট  ",
            },
            db=db,
            current_user=current_user,
        )

        assert result == {
            "success": True,
            "data": expected,
        }

        knowledge_tool.assert_awaited_once_with(
            db=db,
            query="রাস্তার বাতি নষ্ট",
        )


@pytest.mark.parametrize(
    "arguments",
    [
        {},
        {"query": ""},
        {"query": "   "},
        {"query": 123},
        {"query": "A" * 2001},
        {
            "query": "Water supply",
            "citizen_id": 999,
        },
    ],
)
async def test_invalid_arguments_are_rejected(
    dependencies,
    arguments,
):
    db, current_user = dependencies

    with patch(
        "app.integrations.llm.tools.executor."
        "search_published_knowledge",
        new_callable=AsyncMock,
    ) as knowledge_tool:
        result = await execute_ai_tool(
            tool_name="search_published_knowledge",
            arguments=arguments,
            db=db,
            current_user=current_user,
        )

        assert result["success"] is False
        assert result["error"] == (
            "Invalid knowledge search arguments."
        )

        knowledge_tool.assert_not_awaited()


async def test_unknown_tool_is_rejected(
    dependencies,
):
    db, current_user = dependencies

    result = await execute_ai_tool(
        tool_name="delete_all_knowledge",
        arguments={},
        db=db,
        current_user=current_user,
    )

    assert result["success"] is False
    assert result["error"] == (
        "Unknown or unauthorized AI tool."
    )
