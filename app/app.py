import os
import psycopg2
from app.db import get_db, init_db
from flask import Flask, jsonify, request
from app.validation import (
    validate_server_create,
    validate_server_update
)
from app.repository import get_all_servers
from app.repository import delete_server



app = Flask(__name__)


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

    error = validate_server_create(data)
    if error:
        return jsonify(error=error), 400
    
    result = create_server(data)

    return jsonify(message="server added", server = result)
    

@app.route("/servers", methods=["GET"])
def get_servers():
    return jsonify(get_all_servers())

@app.route("/servers/<int:server_id>", methods = ["DELETE"])
def remove_server(server_id):
    deleted = delete_server(server_id)

    if not deleted:
        return jsonify(error = "server not found"), 404

    return jsonify(message = "server deleted")


@app.route("/servers/<int:server_id>", methods=["PUT"])
def modify_server(server_id):
    data = request.get_json()

    error = validate_server_update(data)
    if error:
        return jsonify(error=error), 400
    
    result = update_server(server_id, data)

    if result is None:
        return jsonify(error = "server not found"), 404
    
    return jsonify(message = "server updated", server = result)

init_db()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host = "0.0.0.0", port = port, debug = debug)
    

