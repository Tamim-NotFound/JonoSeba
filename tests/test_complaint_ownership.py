from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import pytest
from app.core.exceptions import NotFoundError
from app.integrations.llm.tools.complaints import (
    get_my_complaint_status,
)
from app.modules.auth.models import UserRole
from app.modules.complaints.services import ComplaintService


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
def admin():
    return SimpleNamespace(
        id=3,
        role=UserRole.ADMIN,
        is_active=True,
    )


@pytest.fixture
def complaint():
    return SimpleNamespace(
        id=15,
        citizen_id=2,
        title="Broken streetlight near my house",
        status=SimpleNamespace(value="pending"),
        priority=SimpleNamespace(value="medium"),
        department_id=4,
        created_at=SimpleNamespace(
            isoformat=lambda: "2026-11-20T10:00:00"
        ),
        updated_at=SimpleNamespace(
            isoformat=lambda: "2026-11-20T10:00:00"
        ),
    )


@pytest.fixture
def fake_db():
    return SimpleNamespace()


def mock_complaint_repository(complaint):
    return patch(
        "app.modules.complaints.services."
        "ComplaintRepository",
        return_value=SimpleNamespace(
            get_by_id=AsyncMock(return_value=complaint)
        ),
    )


async def test_citizen_can_view_own_complaint(
    fake_db,
    citizen,
    complaint,
):
    with mock_complaint_repository(complaint):
        service = ComplaintService(fake_db)

        result = await service.get_by_id(
            complaint_id=15,
            current_user=citizen,
        )

    assert result.id == 15
    assert result.citizen_id == citizen.id


async def test_citizen_cannot_view_other_citizen_complaint(
    fake_db,
    other_citizen,
    complaint,
):
    with mock_complaint_repository(complaint):
        service = ComplaintService(fake_db)

        with pytest.raises(NotFoundError):
            await service.get_by_id(
                complaint_id=15,
                current_user=other_citizen,
            )


async def test_admin_can_view_citizen_complaint(
    fake_db,
    admin,
    complaint,
):
    with mock_complaint_repository(complaint):
        service = ComplaintService(fake_db)

        result = await service.get_by_id(
            complaint_id=15,
            current_user=admin,
        )

    assert result.id == 15
    assert result.citizen_id == 2


async def test_missing_complaint_returns_not_found(
    fake_db,
    citizen,
):
    with mock_complaint_repository(None):
        service = ComplaintService(fake_db)

        with pytest.raises(NotFoundError):
            await service.get_by_id(
                complaint_id=999,
                current_user=citizen,
            )


async def test_ai_tool_hides_other_citizen_complaint(
    fake_db,
    other_citizen,
    complaint,
):
    with mock_complaint_repository(complaint):
        result = await get_my_complaint_status(
            db=fake_db,
            complaint_id=15,
            current_user=other_citizen,
        )

    assert result["found"] is False
    assert "complaint" not in result

    assert complaint.title not in str(result)
    assert complaint.citizen_id != other_citizen.id
