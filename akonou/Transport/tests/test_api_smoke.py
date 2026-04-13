from fastapi.testclient import TestClient

from api.app.main import app


def test_health_ok() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "ok"


def test_kpi_endpoint_ok() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/analytics/kpi")
        assert response.status_code == 200
        payload = response.json()
        assert "total_buses" in payload
        assert "active_buses" in payload
