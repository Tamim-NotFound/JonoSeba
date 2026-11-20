import json
import sys
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


def make_server_parameters():
    """
    Launch MCP using the same virtual environment
    as the test runner.
    """
    return StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "app.integrations.mcp.stdio_server",
        ],
    )


async def test_stdio_discovers_all_tools():
    parameters = make_server_parameters()

    async with stdio_client(parameters) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await session.initialize()

            response = await session.list_tools()

            tool_names = {
                tool.name
                for tool in response.tools
            }

            assert {
                "get_jonoseba_demo_overview",
                "get_active_departments",
                "search_municipal_knowledge",
            }.issubset(tool_names)


async def test_stdio_resource_and_prompt():
    parameters = make_server_parameters()

    async with stdio_client(parameters) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await session.initialize()

            resources = await session.list_resources()

            resource_uris = {
                str(resource.uri)
                for resource in resources.resources
            }

            assert "jonoseba://about" in resource_uris

            resource = await session.read_resource(
                "jonoseba://about"
            )

            assert "JonoSeba" in (
                resource.contents[0].text
            )

            prompts = await session.list_prompts()

            prompt_names = {
                prompt.name
                for prompt in prompts.prompts
            }

            assert (
                "citizen_service_assistant"
                in prompt_names
            )

            prompt = await session.get_prompt(
                "citizen_service_assistant",
                arguments={"language": "bn"},
            )

            assert prompt.messages
            assert "নাগরিকসেবা" in (
                prompt.messages[0].content.text
            )


async def test_stdio_calls_real_department_tool():
    parameters = make_server_parameters()

    async with stdio_client(parameters) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await session.initialize()

            response = await session.call_tool(
                "get_active_departments",
                arguments={},
            )

            assert response.isError is False
            assert response.content

            text_items = [
                item.text
                for item in response.content
                if item.type == "text"
            ]

            assert text_items

            data = json.loads(text_items[0])

            assert isinstance(
                data["departments"],
                list,
            )

            assert data["count"] == len(
                data["departments"]
            )

            assert all(
                department["name"]
                for department in data["departments"]
            )

            print(
                "\nMCP stdio departments:",
                data["count"],
            )


async def test_stdio_demo_overview_tool():
    parameters = make_server_parameters()

    async with stdio_client(parameters) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await session.initialize()

            response = await session.call_tool(
                "get_jonoseba_demo_overview",
                arguments={},
            )

            assert response.isError is False

            text_items = [
                item.text
                for item in response.content
                if item.type == "text"
            ]

            assert text_items

            data = json.loads(text_items[0])

            assert data["name"] == "JonoSeba"
            assert data["mode"] == "demonstration"
