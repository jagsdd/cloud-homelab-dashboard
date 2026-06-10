import os
from flask import Flask, jsonify, request

app = Flask(__name__)

servers = []

@app.route("/")
def home():
     return "Cloud Homelab Dashboard running"

@app.route("/health")
def health():
     return jsonify(status="ok")

@app.route("/servers", methods=["POST"])
def add_server():
	data = request.get_json()
	
	server = {
		"name": data.get("name"),
		"status": data.get("status", "unknown")
	}
	
	servers.append(server)
	return jsonify(message="server added", server=server)

@app.route("/servers", methods=["GET"])
def get_servers():
    return jsonify(servers)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host = "0.0.0.0", port = port, debug = debug)
    

