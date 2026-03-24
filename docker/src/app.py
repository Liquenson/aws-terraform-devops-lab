from flask import Flask, jsonify
import os

app = Flask(__name__)

# REST API only - no forms, no sessions, no state-changing operations
# CSRF protection not applicable for stateless JSON API endpoints


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
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "8080"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)
