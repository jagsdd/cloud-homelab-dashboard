import os
import logging
from app.db import init_db, check_db_connection
from flask import Flask, jsonify, request
from app.service import (
    create_server_service,
    update_server_service,
    delete_server_service,
    get_all_servers_service,
    get_server_service
)
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST



app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

@app.route("/")
def home():
     init_db()
     return "Cloud Homelab Dashboard running"

@app.route("/health")
def health():
     if check_db_connection():
         return jsonify(status="ok")
     return jsonify(status="unhealthy"), 503

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/servers", methods=["POST"])
def add_server():
    result, status = create_server_service(request.get_json(silent=True))
    return jsonify(result), status

@app.route("/servers", methods=["GET"])
def get_servers():
    result, status = get_all_servers_service()
    return jsonify(result), status

@app.route("/servers/<int:server_id>", methods=["GET"])
def get_single_server(server_id):
    result, status = get_server_service(server_id)
    return jsonify(result), status

@app.route("/servers/<int:server_id>", methods = ["DELETE"])
def remove_server(server_id):
    result, status = delete_server_service(server_id)
    return jsonify(result), status

@app.route("/servers/<int:server_id>", methods=["PUT"])
def modify_server(server_id):
    result, status = update_server_service(server_id, request.get_json(silent=True))
    return jsonify(result), status

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host = "0.0.0.0", port = port, debug = debug)
    

