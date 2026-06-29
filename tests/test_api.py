import sys
import os
sys.path.append(os.path.abspath("."))

import pytest
from app.app import app
from app.db import get_db


@pytest.fixture(scope="function")
def client():
    app.config["TESTING"] = True

    conn, cursor = get_db()
    cursor.execute("DELETE FROM servers;")
    conn.commit()
    conn.close()

    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def init_db():
    conn, cursor = get_db()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            status VARCHAR(50)
        )
    """)

    conn.commit()
    conn.close()
    

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_invalid_status(client):
    response = client.put(
        "/servers/1",
        json = {
            "status": "banana"
        }
    )

    assert response.status_code == 400
