import os
from jose import jwt
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_sync.db")

from admin_sync_service.app.main import app

client = TestClient(app)
SECRET = "supersecret"


def make_token():
    return jwt.encode({"sub": "admin@hobbyhosting.org", "is_admin": True}, SECRET, algorithm="HS256")


def test_chat_message_create_and_list():
    token = make_token()
    resp = client.post(
        "/chat/messages",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Hello"
    assert data["username"] == "admin@hobbyhosting.org"

    list_resp = client.get(
        "/chat/messages", headers={"Authorization": f"Bearer {token}"}
    )
    assert list_resp.status_code == 200
    msgs = list_resp.json()
    assert any(m["message"] == "Hello" for m in msgs)
