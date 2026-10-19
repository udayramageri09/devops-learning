from flask import Flask, jsonify
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Response
import random

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "lab_http_requests_total",
    "Total HTTP requests to the lab application"
)

ACTIVE_USERS = Gauge(
    "lab_active_users",
    "Simulated active users"
)

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify(message="DevOps Monitoring Lab", status="running")

@app.route("/simulate")
def simulate():
    REQUEST_COUNT.inc()
    users = random.randint(1, 100)
    ACTIVE_USERS.set(users)
    return jsonify(active_users=users)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


