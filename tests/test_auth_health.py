from fastapi.testclient import TestClient
from auth_service.app.main import app

client = TestClient(app)

def test_auth_health():
    response = client.get("/auth/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
