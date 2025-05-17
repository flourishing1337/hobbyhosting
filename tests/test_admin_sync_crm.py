import os
from fastapi.testclient import TestClient

# Ensure local sqlite DB for testing
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_sync.db")

from admin_sync_service.app.main import app

client = TestClient(app)


def test_create_company_and_todo():
    # Create a company
    comp_resp = client.post(
        "/crm/companies",
        json={"name": "Acme", "status": "active", "notes": "", "contacts": []},
    )
    assert comp_resp.status_code == 200
    company_id = comp_resp.json()["id"]

    # Add todo
    todo_resp = client.post(
        f"/crm/companies/{company_id}/todos",
        json={"title": "Call customer", "due_date": None, "completed": False},
    )
    assert todo_resp.status_code == 200
    todo_data = todo_resp.json()
    assert todo_data["title"] == "Call customer"

    # List todos
    list_resp = client.get(f"/crm/companies/{company_id}/todos")
    assert list_resp.status_code == 200
    todos = list_resp.json()
    assert len(todos) == 1
    assert todos[0]["id"] == todo_data["id"]
