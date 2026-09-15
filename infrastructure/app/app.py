from flask import Flask
import socket

app = Flask(__name__)


@app.route("/")
def home():
    return "Cloud Orchestrator Application is Running!"


@app.route("/health")
def health():
    return "Healthy"


@app.route("/info")
def info():
    return "Container: " + socket.gethostname()


@app.route("/cpu")
def cpu_load():
    total = 0

    for i in range(3000000):
        total += i * i

    return "CPU work completed: " + str(total)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)