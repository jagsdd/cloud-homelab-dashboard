import logging, time
from app.db import check_db_connection
from app.config import PORT, DEBUG
from flask import Flask, jsonify, request, g
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.metrics import REQUEST_COUNT, REQUEST_LATENCY
from app.service import (
    create_server_service,
    update_server_service,
    delete_server_service,
    get_all_servers_service,
    get_server_service
)


app = Flask(__name__)

@app.before_request
def start_timer():
    g.start_time = time.perf_counter()

@app.after_request
def count_request(response):
    REQUEST_COUNT.labels(
        request.method,
        str(response.status_code)
    ).inc()

    REQUEST_LATENCY.observe(
        time.perf_counter() - g.start_time
    )

    return response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

@app.route("/")
def home():
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
    app.run(host="0.0.0.0", port=int(PORT), debug=DEBUG)
    

