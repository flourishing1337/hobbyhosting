import os
from jose import jwt
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_sync.db")

from admin_sync_service.app.main import app

client = TestClient(app)
SECRET = "supersecret"


def make_token():
    return jwt.encode({"sub": "admin@hobbyhosting.org", "is_admin": True}, SECRET, algorithm="HS256")


def test_file_upload_and_list():
    token = make_token()
    resp = client.post(
        "/files",
        headers={"Authorization": f"Bearer {token}"},
        files={"upload_file": ("test.txt", b"hello", "text/plain")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["filename"] == "test.txt"

    list_resp = client.get("/files", headers={"Authorization": f"Bearer {token}"})
    assert list_resp.status_code == 200
    files = list_resp.json()
    assert any(f["filename"] == "test.txt" for f in files)
