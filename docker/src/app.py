from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "app": "devops-lab-webapp",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("AWS_REGION", "local"),
        "status": "ok"
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/ready", methods=["GET"])
def ready():
    return jsonify({"status": "ready"}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
