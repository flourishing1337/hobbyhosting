import os
import uuid

from fastapi.testclient import TestClient

# Ensure required environment variables are set before importing the app
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_auth.db")

from auth_service.app.main import app

client = TestClient(app)

def test_auth_health():
    response = client.get("/auth/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_returns_access_token():
    """Register and log in a user using JSON payloads."""
    username = f"user_{uuid.uuid4().hex}"
    password = "test-pass"

    # Create user first
    reg_resp = client.post(
        "/auth/register",
        json={"username": username, "password": password},
    )
    assert reg_resp.status_code == 201

    # Now log in with the same credentials
    login_resp = client.post(
        "/auth/login",
        json={"username": username, "password": password},
    )
    assert login_resp.status_code == 200
    data = login_resp.json()
    assert "access_token" in data and data["access_token"]
