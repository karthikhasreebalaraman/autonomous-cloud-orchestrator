from flask import Flask, Response
import requests
import subprocess

app = Flask(__name__)

current = 0


def get_backends():

    result = subprocess.run(
        [
            "docker",
            "ps",
            "--format",
            "{{.Names}} {{.Ports}}"
        ],
        capture_output=True,
        text=True
    )

    backends = []

    for line in result.stdout.splitlines():

        parts = line.split(" ", 1)

        if len(parts) != 2:
            continue

        name = parts[0]
        ports = parts[1]

        if name == "cloud-app" or name.startswith("cloud-app-"):

            if "0.0.0.0:" in ports:

                port_part = ports.split("0.0.0.0:")[1]
                port = port_part.split("->")[0]

                backends.append(
                    "http://localhost:" + port
                )

    return backends


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def load_balance(path):

    global current

    backends = get_backends()

    if not backends:
        return "No healthy backend containers available", 503

    current = current % len(backends)

    backend = backends[current]

    current = (current + 1) % len(backends)

    url = backend + "/" + path

    try:

        response = requests.get(
            url,
            timeout=5
        )

        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get(
                "Content-Type"
            )
        )

    except requests.exceptions.RequestException:

        return "Backend unavailable", 503


if __name__ == "__main__":

    print("================================")
    print(" DYNAMIC LOAD BALANCER")
    print("================================")

    app.run(
        host="0.0.0.0",
        port=8000
    )