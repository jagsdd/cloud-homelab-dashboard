import os
import psycopg2
from flask import Flask, jsonify, request


app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

ALLOWED_STATUSES = ["online", "offline", "maintainance"]


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn, conn.cursor()

def validate_server(data):
    if not data:
        return "No input data provided"
    
    name = data.get("name")
    if not name or not name.strip():
        return "Name is required"
    
    status = data.get("status")
    if status and status not in ALLOWED_STATUSES:
        return f"Invalid status. Must be one of {ALLOWED_STATUSES}"
    
    return None

def validate_server_update(data):
    if not data:
        return "No input data provided"
    
    status = data.get("status")
    if status and status not in ALLOWED_STATUSES:
        return f"Invalid status. Must be one of {ALLOWED_STATUSES}"
    
    return None


@app.route("/")
def home():
     init_db()
     return "Cloud Homelab Dashboard running"

@app.route("/health")
def health():
     return jsonify(status="ok")

@app.route("/servers", methods=["POST"])
def add_server():
    data = request.get_json()

    error = validate_server(data)
    if error:
        return jsonify(error=error), 400
    
    conn, cursor = get_db()
    
    cursor.execute(
        "INSERT INTO servers (name, status) VALUES (%s, %s)",
        (data["name"], data.get("status", "unknown"))
    )
    
    conn.commit()
    conn.close()

    return jsonify(message="server added")

@app.route("/servers", methods=["GET"])
def get_servers():
    conn, cursor = get_db()
    
    cursor.execute("SELECT id, name, status FROM servers")
    rows = cursor.fetchall()
    
    conn.close()

    return jsonify([
        {"id": r[0], "name": r[1], "status": r[2]}
        for r in rows
        ])

@app.route("/servers/<int:server_id>", methods = ["DELETE"])
def delete_server(server_id):
    conn, cursor = get_db()

    cursor.execute("DELETE FROM servers WHERE id = %s", (server_id,))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify(error = "server not found"), 404

    conn.commit()
    conn.close()

    return jsonify(message = "server deleted")


@app.route("/servers/<int:server_id>", methods=["PUT"])
def update_server(server_id):
    data = request.get_json()
    
    error = validate_server_update(data)
    if error:
        return jsonify(error=error), 400
    
    conn, cursor = get_db()

    cursor.execute("SELECT id, name, status FROM servers WHERE id = %s", (server_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return jsonify(error = "server not found"), 404
    
    name = data.get("name", row[1])
    status = data.get("status", row[2])

    cursor.execute("UPDATE servers SET name = %s, status = %s WHERE id = %s", (name, status, server_id))

    conn.commit()
    conn.close()

    return jsonify(message = "server updated")


def init_db():
    conn, cursor = get_db()
    
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS servers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                status VARCHAR(50)
                )""")
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host = "0.0.0.0", port = port, debug = debug)
    

