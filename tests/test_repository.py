from unittest.mock import patch, Mock, call
from app.repository import get_server, create_server, delete_server, update_server

def test_get_server():
    mock_conn = Mock()
    mock_cursor = Mock()
    server_id = 1

    mock_cursor.fetchone.return_value = (1, "proxmox", "online")

    with patch("app.repository.get_db") as mock_get_db:
        mock_get_db.return_value = (mock_conn, mock_cursor)

        server = get_server(server_id)

        mock_cursor.execute.assert_called_once_with(
            "SELECT id, name, status FROM servers WHERE id = %s",
            (server_id,)
        )

        assert server["id"] == server_id
        assert server["name"] == "proxmox"
        assert server["status"] == "online"
        mock_conn.close.assert_called_once()

def test_get_server_not_found():
    server_id = 999999
    mock_conn = Mock()
    mock_cursor = Mock()

    mock_cursor.fetchone.return_value = None

    with patch("app.repository.get_db") as mock_get_db:
        mock_get_db.return_value = (mock_conn, mock_cursor)

        server = get_server(server_id)

        mock_cursor.execute.assert_called_once_with(
            "SELECT id, name, status FROM servers WHERE id = %s",
            (server_id,)
        )

        mock_conn.close.assert_called_once()
        assert server is None

def test_create_server():
    data = {
        "name": "proxmox",
        "status": "online"
    }

    mock_conn = Mock()
    mock_cursor = Mock()

    with patch("app.repository.get_db") as mock_get_db:
        mock_get_db.return_value = (mock_conn, mock_cursor)

        mock_cursor.fetchone.return_value = (1,)

        server = create_server(data)

        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO servers (name, status) VALUES (%s, %s) RETURNING id",
            (data["name"], data["status"])
        )

        assert server["id"] == 1
        assert server["name"] == "proxmox"
        assert server["status"] == "online"
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

def test_create_server_no_status():
    data = {
        "name": "proxmox",
    }

    mock_conn = Mock()
    mock_cursor = Mock()

    with patch("app.repository.get_db") as mock_get_db:
        mock_get_db.return_value = (mock_conn, mock_cursor)

        mock_cursor.fetchone.return_value = (1,)

        server = create_server(data)

        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO servers (name, status) VALUES (%s, %s) RETURNING id",
            (data["name"], "unknown")
        )

        assert server["id"] == 1
        assert server["name"] == "proxmox"
        assert server["status"] == "unknown"
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

def test_delete_server():
    server_id = 1

    mock_conn = Mock()
    mock_cursor = Mock()

    with patch("app.repository.get_db") as mock_get_db:
        mock_get_db.return_value = (mock_conn, mock_cursor)

        mock_cursor.rowcount = 1

        deleted = delete_server(server_id)

        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM servers WHERE id = %s",
            (server_id,)
        )

        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        assert deleted is True

def test_delete_server_not_found():
    server_id = 999999

    mock_conn = Mock()
    mock_cursor = Mock()

    with patch("app.repository.get_db") as mock_get_db:
        mock_get_db.return_value = (mock_conn, mock_cursor)

        mock_cursor.rowcount = 0

        deleted = delete_server(server_id)

        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM servers WHERE id = %s",
            (server_id,)
        )

        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        assert deleted is False

def test_update_server():
    server_id = 1
    data = {
        "status": "offline"
    }
    
    mock_conn = Mock()
    mock_cursor = Mock()

    with patch("app.repository.get_db") as mock_get_db:
        mock_get_db.return_value = (mock_conn, mock_cursor)

        mock_cursor.fetchone.return_value = (1, "proxmox", "online")

        server = update_server(server_id, data)

        assert mock_cursor.execute.call_args_list[0] == call("SELECT id, name, status FROM servers WHERE id = %s",
                                                             (server_id,))

        assert mock_cursor.execute.call_args_list[1] == call("UPDATE servers SET name = %s, status = %s WHERE id = %s",
                                                             ("proxmox", data["status"], server_id))
        assert server["id"] == 1
        assert server["name"] == "proxmox"
        assert server["status"] == data["status"]
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

def test_update_server_not_found():
    server_id = 999999
    data = {
        "status": "offline"
    }
    
    mock_conn = Mock()
    mock_cursor = Mock()

    with patch("app.repository.get_db") as mock_get_db:
        mock_get_db.return_value = (mock_conn, mock_cursor)

        mock_cursor.fetchone.return_value = None

        server = update_server(server_id, data)

        mock_cursor.execute.assert_called_once_with("SELECT id, name, status FROM servers WHERE id = %s",
                                                  (server_id,))
        
        assert len(mock_cursor.execute.call_args_list) == 1
        assert server is None
        mock_conn.close.assert_called_once()

