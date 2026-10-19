from flask import Flask, jsonify
import os
import redis
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Docker Networking Lab", status="running")

@app.route("/check")
def check():
    results = {}

    try:
        cache = redis.Redis(
            host=os.getenv("REDIS_HOST", "lab-redis"),
            port=6379,
            socket_connect_timeout=5
        )
        results["redis"] = "connected" if cache.ping() else "failed"
    except Exception as exc:
        results["redis"] = f"error: {exc}"

    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "lab-mysql"),
            user="root",
            password=os.environ["MYSQL_PASSWORD"],
            database="devops_lab",
            connection_timeout=5
        )
        results["mysql"] = "connected" if connection.is_connected() else "failed"
        connection.close()
    except Exception as exc:
        results["mysql"] = f"error: {exc}"

    status = 200 if results.get("mysql") == "connected" and results.get("redis") == "connected" else 503
    return jsonify(results), status

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
