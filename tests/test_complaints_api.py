from datetime import datetime, timezone
from types import SimpleNamespace
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import UserRole
from app.modules.complaints.dependencies import get_complaint_service


COMPLAINT_URL = "/api/v1/complaints"

CITIZEN = SimpleNamespace(
    id=2,
    role=UserRole.CITIZEN,
    is_active=True,
)

ADMIN = SimpleNamespace(
    id=3,
    role=UserRole.ADMIN,
    is_active=True,
)

COMPLAINT_DATA = {
    "title": "No water supply in our area",
    "description": "There has been no drinking water for three days.",
    "location": "Savar, Dhaka",
    "department_id": 1,
}


def make_complaint(
    citizen_id=2,
    status="pending",
    priority="medium",
):
    now = datetime.now(timezone.utc)

    return {
        "id": 1,
        "title": COMPLAINT_DATA["title"],
        "description": COMPLAINT_DATA["description"],
        "location": COMPLAINT_DATA["location"],
        "status": status,
        "priority": priority,
        "citizen_id": citizen_id,
        "department_id": 1,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }


class FakeComplaintService:
    async def create(self, data, current_user):
        return make_complaint(
            citizen_id=current_user.id,
        )

    async def get_all(
        self,
        current_user,
        search=None,
        status=None,
        priority=None,
        department_id=None,
    ):
        return [
            make_complaint(
                citizen_id=current_user.id,
            )
        ]

    async def get_by_id(
        self,
        complaint_id,
        current_user,
    ):
        return make_complaint(
            citizen_id=current_user.id,
        )

    async def update(
        self,
        complaint_id,
        data,
        current_user,
    ):
        return make_complaint(
            status=data.status or "pending",
            priority=data.priority or "medium",
        )

    async def delete(
        self,
        complaint_id,
        current_user,
    ):
        return None


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def fake_service():
    service = FakeComplaintService()

    app.dependency_overrides[
        get_complaint_service
    ] = lambda: service

    yield service

    app.dependency_overrides.clear()


def authorize_as(user):
    app.dependency_overrides[
        get_current_user
    ] = lambda: user


def test_anonymous_user_cannot_create_complaint(
    client,
    fake_service,
):
    response = client.post(
        COMPLAINT_URL,
        json=COMPLAINT_DATA,
    )

    assert response.status_code == 401


def test_citizen_can_create_complaint(
    client,
    fake_service,
):
    authorize_as(CITIZEN)

    response = client.post(
        COMPLAINT_URL,
        json=COMPLAINT_DATA,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == COMPLAINT_DATA["title"]
    assert body["citizen_id"] == CITIZEN.id
    assert body["status"] == "pending"


def test_citizen_can_list_complaints(
    client,
    fake_service,
):
    authorize_as(CITIZEN)

    response = client.get(COMPLAINT_URL)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["citizen_id"] == CITIZEN.id


def test_citizen_cannot_update_complaint(
    client,
    fake_service,
):
    authorize_as(CITIZEN)

    response = client.patch(
        f"{COMPLAINT_URL}/1",
        json={
            "status": "in_progress",
            "priority": "high",
        },
    )

    assert response.status_code == 403


def test_admin_can_update_complaint(
    client,
    fake_service,
):
    authorize_as(ADMIN)

    response = client.patch(
        f"{COMPLAINT_URL}/1",
        json={
            "status": "in_progress",
            "priority": "high",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "in_progress"
    assert body["priority"] == "high"



def test_anonymous_user_cannot_list_complaints(
    client,
    fake_service,
):
    response = client.get(COMPLAINT_URL)

    assert response.status_code == 401


def test_citizen_cannot_delete_complaint(
    client,
    fake_service,
):
    authorize_as(CITIZEN)

    response = client.delete(
        f"{COMPLAINT_URL}/1"
    )

    assert response.status_code == 403


def test_admin_can_delete_complaint(
    client,
    fake_service,
):
    authorize_as(ADMIN)

    response = client.delete(
        f"{COMPLAINT_URL}/1"
    )

    assert response.status_code == 204
    assert response.content == b""


def test_invalid_complaint_title_is_rejected(
    client,
    fake_service,
):
    authorize_as(CITIZEN)

    invalid_data = {
        **COMPLAINT_DATA,
        "title": "Bad",
    }

    response = client.post(
        COMPLAINT_URL,
        json=invalid_data,
    )

    assert response.status_code == 422


def test_invalid_complaint_status_is_rejected(
    client,
    fake_service,
):
    authorize_as(ADMIN)

    response = client.patch(
        f"{COMPLAINT_URL}/1",
        json={
            "status": "finished",
        },
    )

    assert response.status_code == 422


def test_invalid_complaint_id_is_rejected(
    client,
    fake_service,
):
    authorize_as(CITIZEN)

    response = client.get(
        f"{COMPLAINT_URL}/abc"
    )

    assert response.status_code == 422
