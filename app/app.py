import os
import psycopg2
from flask import Flask, jsonify, request


app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn, conn.cursor()

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
    

