import requests

def test_health_endpoint():
    response = requests.get("http://localhost:5000/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_server_valid():
    r = requests.post(
        "http://localhost:5000/servers",
        json = {"name": "proxmox", "status": "online"}
    )
    assert r.status_code == 201

    data = r.json()

    assert data["message"] == "server added"
    assert data["server"]["id"] is not None
    assert data["server"]["name"] == "proxmox"
    assert data["server"]["status"] == "online"

def test_create_server_missing_name():
    r = requests.post(
        "http://localhost:5000/servers",
        json = {"status": "online"}
    )
    assert r.status_code == 400

def test_create_server_invalid_status():
    r = requests.post(
        "http://localhost:5000/servers",
        json = {"name": "nas", "status": "broken"}
    )
    assert r.status_code == 400

def test_update_server_valid():
    r = requests.post(
        "http://localhost:5000/servers",
        json = {"name": "proxmox", "status": "online"}
    )
    assert r.status_code == 201

    data = r.json()
    server_id = data["server"]["id"]

    r = requests.put(
        f"http://localhost:5000/servers/{server_id}",
        json = {"status": "offline"}
    )
    assert r.status_code == 200
    data = r.json()
    assert data["server"]["status"] == "offline"

def test_update_server_not_found():
    r = requests.put(
        "http://localhost:5000/servers/999999",
        json={"status": "offline"}
    )
    assert r.status_code == 404
    assert r.json()["error"] == "server not found"

def test_update_server_invalid_status():
    r = requests.post(
        "http://localhost:5000/servers",
        json = {"name": "proxmox", "status": "online"}
    )
    assert r.status_code == 201

    data = r.json()
    server_id = data["server"]["id"]

    r = requests.put(
        f"http://localhost:5000/servers/{server_id}",
        json = {"status": "broken"}
    )
    assert r.status_code == 400
    assert "invalid" in r.json()["error"].lower()

def test_get_server():
    r = requests.post(
        "http://localhost:5000/servers",
        json = {"name": "proxmox", "status": "online"}
    )
    assert r.status_code == 201

    data = r.json()
    server_id =data["server"]["id"]

    r = requests.get(
        f"http://localhost:5000/servers/{server_id}",   
    )
    assert r.status_code ==200
    data = r.json()
    assert data["server"]["id"] == server_id
    assert data["server"]["name"] == "proxmox"
    assert data["server"]["status"] == "online"

def test_get_invalid_server():
    r = requests.get(
        "http://localhost:5000/servers/999999",
    )
    assert r.status_code == 404
    assert r.json()["error"] == "server not found"

def test_delete_server():
    r = requests.post(
        "http://localhost:5000/servers",
        json = {"name": "proxmox", "status": "online"}
    )

    assert r.status_code == 201

    data = r.json()
    server_id = data["server"]["id"]

    r = requests.delete(
        f"http://localhost:5000/servers/{server_id}"
    )

    assert r.status_code == 200
    data = r.json()
    assert data["message"] == "server deleted"

    r = requests.get(
        f"http://localhost:5000/servers/{server_id}"
    )
    assert r.status_code == 404
    assert r.json()["error"] == "server not found"

def test_delete_server_not_found():
    r = requests.delete(
        "http://localhost:5000/servers/999999"
    )
    assert r.status_code == 404
    assert r.json()["error"] == "server not found"