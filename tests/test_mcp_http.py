from unittest.mock import patch
import pytest
from app.integrations.mcp.http_server import (
    MCP_HTTP_HOST,
    MCP_HTTP_PATH,
    MCP_HTTP_PORT,
    configure_http_server,
    main,
)
from app.integrations.mcp.server import mcp


def test_mcp_http_configuration():
    server = configure_http_server()

    assert server is mcp
    assert server.settings.host == "127.0.0.1"
    assert server.settings.port == 8001
    assert server.settings.streamable_http_path == "/mcp"
    assert server.settings.stateless_http is True


def test_http_server_uses_streamable_http_transport():
    with patch.object(mcp, "run") as run_mock:
        main()

    run_mock.assert_called_once_with(
        transport="streamable-http"
    )


@pytest.mark.anyio
async def test_http_server_preserves_registered_tools():
    configure_http_server()

    registered_tools = await mcp.list_tools()

    names = {
        tool.name
        for tool in registered_tools
    }

    assert {
        "get_jonoseba_demo_overview",
        "get_active_departments",
        "search_municipal_knowledge",
    }.issubset(names)


@pytest.mark.anyio
async def test_http_server_preserves_resource_and_prompt():
    configure_http_server()

    resources = await mcp.list_resources()
    prompts = await mcp.list_prompts()

    resource_uris = {
        str(resource.uri)
        for resource in resources
    }

    prompt_names = {
        prompt.name
        for prompt in prompts
    }

    assert "jonoseba://about" in resource_uris
    assert "citizen_service_assistant" in prompt_names


@pytest.fixture
def anyio_backend():
    return "asyncio"
