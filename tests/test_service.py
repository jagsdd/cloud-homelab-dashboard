from unittest.mock import patch
from app.service import create_server_service, update_server_service
from app.validation import ALLOWED_STATUSES



def test_create_server_service_valid():
    data = {
        "name": "proxmox",
        "status": "online"
    }

    with patch("app.service.create_server") as mock_create_server:
        mock_create_server.return_value = {
            "id": 1,
            "name": "proxmox",
            "status": "online"
        }
        response, status = create_server_service(data)

        mock_create_server.assert_called_once_with(data)
        
        assert status == 201
        assert response["message"] == "server added"
        
        assert response["server"]["id"] == 1
        assert response["server"]["name"] == "proxmox"
        assert response["server"]["status"] == "online"

def test_create_server_service_invalid():
    data = {
        "status": "online"
    }

    with patch("app.service.create_server") as mock_create_server:
        response, status = create_server_service(data)

        mock_create_server.assert_not_called()
        assert status == 400
        assert response["error"] == "Name is required"


def test_update_server_service_valid():
    server_id = 1

    data = {
        "status": "offline",
    }

    with patch("app.service.update_server") as mock_update_server:
        mock_update_server.return_value = {
            "id": 1,
            "name": "proxmox",
            "status": "offline"
        }

        response, status = update_server_service(server_id, data)

        mock_update_server.assert_called_once_with(server_id, data)

        assert status == 200
        assert response["message"] == "server updated"

        assert response["server"]["id"] == 1
        assert response["server"]["name"] == "proxmox"
        assert response["server"]["status"] == "offline"

def test_update_server_service_no_data():
    server_id = 1

    data = None

    with patch("app.service.update_server") as mock_update_server:
        response, status = update_server_service(server_id, data)

        mock_update_server.assert_not_called()
        assert status == 400
        assert response["error"] == "Invalid JSON"

def test_update_server_service_invalid():
    server_id = 1

    data = {
        "status": "broken",
    }

    with patch("app.service.update_server") as mock_update_server:
        response, status = update_server_service(server_id, data)

        mock_update_server.assert_not_called()
        assert status == 400
        assert response["error"] == f"Invalid status. Must be one of {sorted(ALLOWED_STATUSES)}"

def test_update_server_service_not_found():
    server_id = 999999

    data = {
        "status": "offline"
    }

    with patch("app.service.update_server") as mock_update_server:
        mock_update_server.return_value = None

        response, status = update_server_service(server_id, data)

        mock_update_server.assert_called_once_with(server_id, data)
        assert status == 404
        assert response["error"] == "server not found"
