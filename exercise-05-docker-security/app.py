from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return "Hello from the Exercise 05 Docker security lab!"


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
