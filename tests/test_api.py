from unittest.mock import patch

import pytest
from app.app import app


@pytest.fixture(scope="function")
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    with patch("app.app.check_db_connection") as mock_check_db_connection:
        mock_check_db_connection.return_value = True

        response = client.get("/health")

        mock_check_db_connection.assert_called_once_with()
        assert response.status_code == 200
        assert response.get_json() == {"status": "ok"}

def test_health_endpoint_db_unhealthy(client):
    with patch("app.app.check_db_connection") as mock_check_db_connection:
        mock_check_db_connection.return_value = False

        response = client.get("/health")

        mock_check_db_connection.assert_called_once_with()
        assert response.status_code == 503
        assert response.get_json() == {"status": "unhealthy"}

def test_create_server(client):
    with patch("app.app.create_server_service") as mock_create_server_service:
        mock_create_server_service.return_value = (
            {
                "message": "server added",
                "server": {
                    "id": 1,
                    "name": "proxmox",
                    "status": "online"
                }
            },
            201
        )

        response = client.post(
            "/servers",
            json={"name": "proxmox"}
        )
        mock_create_server_service.assert_called_once_with(
            {"name": "proxmox"}
        )
        assert response.status_code == 201
        assert response.get_json() == {
            "message": "server added",
            "server": {
                "id": 1,
                "name": "proxmox",
                "status": "online"
            }
        }



def test_update_server_returns_service_error(client):
    with patch("app.app.update_server_service") as mock_update_server_service:
        mock_update_server_service.return_value = (
            {"error": "Invalid status. Must be one of ['maintenance', 'offline', 'online']"},
            400
        )

        response = client.put(
            "/servers/1",
            json={"status": "banana"}
        )
        mock_update_server_service.assert_called_once_with(1, {"status": "banana"})
        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid status. Must be one of ['maintenance', 'offline', 'online']"}
