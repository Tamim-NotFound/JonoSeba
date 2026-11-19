from types import SimpleNamespace
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from google.genai.errors import ServerError
from app.main import app
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import UserRole
from app.modules.chat.services import ChatService

CHAT_URL = "/api/v1/chat"

CITIZEN = SimpleNamespace(
    id=2,
    role=UserRole.CITIZEN,
    is_active=True,
)

VALID_REQUEST = {
    "message": "How can I report a broken streetlight?",
    "history": [],
}


@pytest.fixture
def client():
    app.dependency_overrides.clear()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def authorize_as_citizen():
    app.dependency_overrides[get_current_user] = (
        lambda: CITIZEN
    )


def test_anonymous_user_cannot_chat(client):
    response = client.post(
        CHAT_URL,
        json=VALID_REQUEST,
    )

    assert response.status_code == 401


def test_citizen_can_chat(client):
    authorize_as_citizen()

    async def fake_chat(self, data):
        return {
            "reply": "You can submit a streetlight complaint.",
            "model": "gemini-3.1-flash-lite",
        }

    with patch.object(ChatService, "chat", fake_chat):
        response = client.post(
            CHAT_URL,
            json=VALID_REQUEST,
        )

    assert response.status_code == 200
    assert "streetlight" in response.json()["reply"]
    assert response.json()["model"] == (
        "gemini-3.1-flash-lite"
    )


def test_citizen_can_send_conversation_history(client):
    authorize_as_citizen()

    request_body = {
        "message": "What problem did I mention earlier?",
        "history": [
            {
                "role": "user",
                "content": "My streetlight is broken.",
            },
            {
                "role": "model",
                "content": "You can report it through JonoSeba.",
            },
        ],
    }

    async def fake_chat(self, data):
        assert len(data.history) == 2
        assert data.history[0].role == "user"
        assert data.history[1].role == "model"

        return {
            "reply": "You mentioned a broken streetlight.",
            "model": "gemini-3.1-flash-lite",
        }

    with patch.object(ChatService, "chat", fake_chat):
        response = client.post(
            CHAT_URL,
            json=request_body,
        )

    assert response.status_code == 200
    assert "broken streetlight" in response.json()["reply"]


def test_empty_message_is_rejected(client):
    authorize_as_citizen()

    response = client.post(
        CHAT_URL,
        json={
            "message": "",
            "history": [],
        },
    )

    assert response.status_code == 422


def test_invalid_history_role_is_rejected(client):
    authorize_as_citizen()

    response = client.post(
        CHAT_URL,
        json={
            "message": "Hello",
            "history": [
                {
                    "role": "admin",
                    "content": "Previous message",
                }
            ],
        },
    )

    assert response.status_code == 422


def test_too_many_history_messages_are_rejected(client):
    authorize_as_citizen()

    history = [
        {
            "role": "user",
            "content": f"Message {i}",
        }
        for i in range(21)
    ]

    response = client.post(
        CHAT_URL,
        json={
            "message": "Hello",
            "history": history,
        },
    )

    assert response.status_code == 422


def test_gemini_unavailable_returns_503(client):
    authorize_as_citizen()

    class FakeGeminiClient:
        def generate_response(self, message, history):
            raise ServerError(
                503,
                {
                    "error": {
                        "code": 503,
                        "message": "Service unavailable",
                        "status": "UNAVAILABLE",
                    }
                },
                None,
            )

        def close(self):
            pass

    with patch(
        "app.modules.chat.services.GeminiLLMClient",
        FakeGeminiClient,
    ):
        response = client.post(
            CHAT_URL,
            json=VALID_REQUEST,
        )

    assert response.status_code == 503
    assert response.json() == {
        "detail": (
            "JonoSeba AI is temporarily unavailable. "
            "Please try again later."
        )
    }
    assert response.headers["retry-after"] == "30"
