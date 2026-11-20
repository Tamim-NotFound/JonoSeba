from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.integrations.mcp.server import (
    fetch_active_departments,
    mcp,
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fake_database():
    session = MagicMock()
    session.execute = AsyncMock()

    result = MagicMock()
    result.scalars.return_value.all.return_value = []

    session.execute.return_value = result

    factory = MagicMock()
    factory.return_value.__aenter__ = AsyncMock(
        return_value=session
    )
    factory.return_value.__aexit__ = AsyncMock(
        return_value=False
    )

    with patch(
        "app.integrations.mcp.server.AsyncSessionLocal",
        factory,
    ):
        yield session, result


@pytest.mark.anyio
async def test_fetch_active_departments_returns_data(
    fake_database,
):
    session, result = fake_database

    result.scalars.return_value.all.return_value = [
        SimpleNamespace(
            id=1,
            name="Roads and Infrastructure",
            description="Road maintenance services",
        ),
        SimpleNamespace(
            id=2,
            name="Water Supply",
            description="Water supply services",
        ),
    ]

    response = await fetch_active_departments()

    assert response["count"] == 2
    assert len(response["departments"]) == 2

    assert response["departments"][0]["name"] == (
        "Roads and Infrastructure"
    )
    assert response["departments"][1]["name"] == (
        "Water Supply"
    )

    session.execute.assert_awaited_once()


@pytest.mark.anyio
async def test_no_active_departments_returns_empty_list(
    fake_database,
):
    session, result = fake_database

    response = await fetch_active_departments()

    assert response["count"] == 0
    assert response["departments"] == []

    session.execute.assert_awaited_once()


@pytest.mark.anyio
async def test_query_filters_inactive_departments(
    fake_database,
):
    session, _ = fake_database

    await fetch_active_departments()
    statement = session.execute.await_args.args[0]
    compiled = statement.compile()
    sql = str(compiled).lower()

    assert "is_active" in sql
    assert "true" in sql
    assert "order by" in sql


@pytest.mark.anyio
async def test_mcp_registers_department_tool():
    registered = await mcp.list_tools()

    tool_names = {
        tool.name
        for tool in registered
    }

    assert "get_jonoseba_demo_overview" in tool_names
    assert "get_active_departments" in tool_names
