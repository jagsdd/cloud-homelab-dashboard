import requests

def test_health_endpoint():
    response = requests.get("http://localhost:5000/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_server_valid():
    r = requests.post(
        "http://localhost:5000/servers",
        json = {"name": "promox", "status": "online"}
    )
    assert r.status_code == 201

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
        json = {"name": "promox", "status": "online"}
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


    