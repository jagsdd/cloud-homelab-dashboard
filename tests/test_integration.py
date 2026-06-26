import requests

def test_health_endpoint():
    response = requests.get("http://localhost:5000/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}