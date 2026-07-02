from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from app.main import app
from app.services.workspace_service import WorkspaceService


def test_health_ok():
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "db_connected" in response.json()


def test_health_ok_when_workspace_table_missing(monkeypatch):
    def raise_missing_table(*args, **kwargs):
        raise OperationalError("select * from workspaces", {}, Exception("no such table: workspaces"))

    monkeypatch.setattr(WorkspaceService, "current_workspace", raise_missing_table)
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["workspace_loaded"] is False
