from unittest.mock import patch
from app.service import create_server_service


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