from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import pytest
from app.core.exceptions import NotFoundError
from app.integrations.llm.tools.executor import (
    execute_ai_tool,
)
from app.modules.auth.models import UserRole


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def citizen():
    return SimpleNamespace(
        id=2,
        role=UserRole.CITIZEN,
        is_active=True,
    )


@pytest.fixture
def other_citizen():
    return SimpleNamespace(
        id=99,
        role=UserRole.CITIZEN,
        is_active=True,
    )


@pytest.fixture
def fake_db():
    return SimpleNamespace()


async def test_department_tool_executes(
    fake_db,
    citizen,
):
    fake_result = {
        "departments": [
            {
                "id": 4,
                "name": "Street Lighting",
                "description": "Streetlight maintenance",
            }
        ],
        "count": 1,
    }

    with patch(
        "app.integrations.llm.tools.executor.list_departments",
        new_callable=AsyncMock,
        return_value=fake_result,
    ) as mock_tool:
        result = await execute_ai_tool(
            tool_name="list_departments",
            arguments={"search": "Street"},
            db=fake_db,
            current_user=citizen,
        )

    assert result["success"] is True
    assert result["data"]["count"] == 1
    assert result["data"]["departments"][0]["name"] == (
        "Street Lighting"
    )

    mock_tool.assert_awaited_once_with(
        db=fake_db,
        search="Street",
    )


async def test_citizen_can_check_own_complaint(
    fake_db,
    citizen,
):
    fake_result = {
        "found": True,
        "complaint": {
            "id": 15,
            "title": "Broken streetlight",
            "status": "pending",
            "priority": "medium",
            "department_id": 4,
        },
    }

    with patch(
        "app.integrations.llm.tools.executor."
        "get_my_complaint_status",
        new_callable=AsyncMock,
        return_value=fake_result,
    ) as mock_tool:
        result = await execute_ai_tool(
            tool_name="get_my_complaint_status",
            arguments={"complaint_id": 15},
            db=fake_db,
            current_user=citizen,
        )

    assert result["success"] is True
    assert result["data"]["found"] is True
    assert result["data"]["complaint"]["id"] == 15

    mock_tool.assert_awaited_once_with(
        db=fake_db,
        complaint_id=15,
        current_user=citizen,
    )


async def test_other_citizen_complaint_is_hidden(
    fake_db,
    citizen,
    other_citizen,
):
    complaint = SimpleNamespace(
        id=15,
        citizen_id=other_citizen.id,
        title="Private complaint",
        status=SimpleNamespace(value="pending"),
        priority=SimpleNamespace(value="medium"),
        department_id=4,
    )

    async def fake_get_by_id(
        self,
        complaint_id,
        current_user,
    ):
        assert complaint_id == complaint.id

        if current_user.id != complaint.citizen_id:
            raise NotFoundError("Complaint not found.")

        return complaint

    with patch(
        "app.integrations.llm.tools.complaints."
        "ComplaintService.get_by_id",
        fake_get_by_id,
    ):
        result = await execute_ai_tool(
            tool_name="get_my_complaint_status",
            arguments={"complaint_id": 15},
            db=fake_db,
            current_user=citizen,
        )

    assert result["success"] is True
    assert result["data"]["found"] is False
    assert "complaint" not in result["data"]

    assert "Private complaint" not in str(result)


async def test_gemini_cannot_override_citizen_id(
    fake_db,
    citizen,
):
    with patch(
        "app.integrations.llm.tools.executor."
        "get_my_complaint_status",
        new_callable=AsyncMock,
    ) as mock_tool:
        result = await execute_ai_tool(
            tool_name="get_my_complaint_status",
            arguments={
                "complaint_id": 15,
                "citizen_id": 99,
            },
            db=fake_db,
            current_user=citizen,
        )

    assert result["success"] is False
    mock_tool.assert_not_awaited()


async def test_unknown_tool_is_rejected(
    fake_db,
    citizen,
):
    result = await execute_ai_tool(
        tool_name="delete_complaint",
        arguments={"complaint_id": 15},
        db=fake_db,
        current_user=citizen,
    )

    assert result["success"] is False
    assert result["error"] == (
        "Unknown or unauthorized AI tool."
    )
