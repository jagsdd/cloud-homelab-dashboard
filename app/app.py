import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Cloud Homelab Dashboard running"

@app.route("/health")
def health():
    return jsonify(status = "ok")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host = "0.0.0.0", port = port, debug = debug)
    

