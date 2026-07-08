import os
from app.db import init_db
from flask import Flask, jsonify, request
from app.repository import get_all_servers
from app.service import (create_server_service, update_server_service, delete_server_service)



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
    result, status = create_server_service(request.get_json(silent=True))
    return jsonify(result), status


@app.route("/servers", methods=["GET"])
def get_servers():
    return jsonify(get_all_servers())

@app.route("/servers/<int:server_id>", methods = ["DELETE"])
def remove_server(server_id):
    result, status = delete_server_service(server_id)
    return jsonify(result), status


@app.route("/servers/<int:server_id>", methods=["PUT"])
def modify_server(server_id):
    result, status = update_server_service(server_id, request.get_json(silent=True))
    return jsonify(result), status


init_db()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host = "0.0.0.0", port = port, debug = debug)
    

