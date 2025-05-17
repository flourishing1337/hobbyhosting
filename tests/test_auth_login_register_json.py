import os
import uuid

from fastapi.testclient import TestClient

# Ensure required environment variables are set before importing the app
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_auth.db")

from auth_service.app.main import app

client = TestClient(app)


def test_register_json_returns_id_and_message():
    username = f"user_{uuid.uuid4().hex}"
    resp = client.post(
        "/auth/register",
        json={"username": username, "password": "test-pass"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data.get("message") == "User created"


def test_login_json_returns_access_token():
    username = f"user_{uuid.uuid4().hex}"
    password = "test-pass"
    # Register user first
    reg_resp = client.post(
        "/auth/register",
        json={"username": username, "password": password},
    )
    assert reg_resp.status_code == 201

    login_resp = client.post(
        "/auth/login",
        json={"username": username, "password": password},
    )
    assert login_resp.status_code == 200
    data = login_resp.json()
    assert "access_token" in data and data["access_token"]

