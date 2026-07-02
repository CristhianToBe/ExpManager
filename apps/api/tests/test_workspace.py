from fastapi.testclient import TestClient
from app.main import app


def test_workspace_init_creates_files(tmp_path):
    client = TestClient(app)
    workspace = tmp_path / "Expedientes"
    response = client.post("/api/v1/workspace/init", json={"root_path": str(workspace), "profile_display_name": "Usuario Prueba"})
    assert response.status_code == 200
    data = response.json()
    assert data["db_initialized"] is True
    assert data["profile"]["display_name"] == "Usuario Prueba"
    assert (workspace / ".gestor" / "gestor.db").exists()
    assert (workspace / ".gestor" / "config.json").exists()
    assert (workspace / ".gestor" / "logs").is_dir()


def test_validate_path_accepts_inside_workspace(tmp_path):
    client = TestClient(app)
    workspace = tmp_path / "Expedientes"
    client.post("/api/v1/workspace/init", json={"root_path": str(workspace)})
    response = client.post("/api/v1/workspace/validate-path", json={"path": ".gestor/config.json"})
    assert response.status_code == 200
    assert response.json()["is_valid"] is True
    assert response.json()["normalized_relative_path"] == ".gestor/config.json"


def test_validate_path_rejects_traversal_or_outside_workspace(tmp_path):
    client = TestClient(app)
    workspace = tmp_path / "Expedientes"
    outside = tmp_path / "outside.txt"
    outside.write_text("x", encoding="utf-8")
    client.post("/api/v1/workspace/init", json={"root_path": str(workspace)})
    traversal = client.post("/api/v1/workspace/validate-path", json={"path": "../outside.txt"})
    absolute = client.post("/api/v1/workspace/validate-path", json={"path": str(outside)})
    assert traversal.status_code == 200
    assert traversal.json()["is_valid"] is False
    assert absolute.status_code == 200
    assert absolute.json()["is_valid"] is False
