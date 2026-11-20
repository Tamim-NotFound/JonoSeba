from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.integrations.mcp.server import (
    fetch_municipal_knowledge,
    mcp,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fake_dependencies():
    db = MagicMock()

    session_context = MagicMock()
    session_context.__aenter__ = AsyncMock(
        return_value=db
    )
    session_context.__aexit__ = AsyncMock(
        return_value=False
    )

    session_factory = MagicMock(
        return_value=session_context
    )

    with (
        patch(
            "app.integrations.mcp.server.AsyncSessionLocal",
            session_factory,
        ),
        patch(
            "app.integrations.mcp.server."
            "retrieve_published_knowledge",
            new_callable=AsyncMock,
        ) as knowledge_tool,
    ):
        yield db, session_factory, knowledge_tool


async def test_knowledge_search_returns_results(
    fake_dependencies,
):
    db, session_factory, knowledge_tool = (
        fake_dependencies
    )

    knowledge_tool.return_value = {
        "status": "knowledge_found",
        "results": [
            {
                "document_title": "Service Guide",
                "content": "Test municipal information",
                "source_url": "https://example.org/test-only",
            }
        ],
    }

    result = await fetch_municipal_knowledge(
        "Birth registration"
    )

    assert result["status"] == "knowledge_found"
    assert len(result["results"]) == 1
    assert "demonstration knowledge" in result["notice"]

    knowledge_tool.assert_awaited_once_with(
        db=db,
        query="Birth registration",
    )

    session_factory.assert_called_once()


async def test_no_knowledge_returns_empty_results(
    fake_dependencies,
):
    _, _, knowledge_tool = fake_dependencies

    knowledge_tool.return_value = {
        "status": "no_verified_knowledge_found",
        "results": [],
    }

    result = await fetch_municipal_knowledge(
        "Unknown municipal service"
    )

    assert result["results"] == []
    assert result["status"] == (
        "no_verified_knowledge_found"
    )


async def test_bangla_query_is_trimmed(
    fake_dependencies,
):
    db, _, knowledge_tool = fake_dependencies

    knowledge_tool.return_value = {
        "status": "no_verified_knowledge_found",
        "results": [],
    }

    await fetch_municipal_knowledge(
        "  জন্ম নিবন্ধনের নিয়ম কী?  "
    )

    knowledge_tool.assert_awaited_once_with(
        db=db,
        query="জন্ম নিবন্ধনের নিয়ম কী?",
    )


@pytest.mark.parametrize(
    "query",
    [
        "",
        "   ",
        "A" * 2001,
        None,
    ],
)
async def test_invalid_query_is_rejected(
    fake_dependencies,
    query,
):
    _, session_factory, knowledge_tool = (
        fake_dependencies
    )

    with pytest.raises(ValueError):
        await fetch_municipal_knowledge(query)

    session_factory.assert_not_called()
    knowledge_tool.assert_not_awaited()


async def test_mcp_registers_knowledge_tool():
    registered = await mcp.list_tools()

    tool_names = {
        tool.name
        for tool in registered
    }

    assert "get_jonoseba_demo_overview" in tool_names
    assert "get_active_departments" in tool_names
    assert "search_municipal_knowledge" in tool_names
