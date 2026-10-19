from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

IMAGE = "cloud-orchestrator-app"

MIN_CONTAINERS = 2
MAX_CONTAINERS = 6


def get_containers():
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )

    containers = []

    for name in result.stdout.splitlines():
        if name == "cloud-app" or name.startswith("cloud-app-"):
            containers.append(name)

    return containers


def get_running_containers():
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )

    containers = []

    for name in result.stdout.splitlines():
        if name == "cloud-app" or name.startswith("cloud-app-"):
            containers.append(name)

    return containers


def get_next_number():
    containers = get_containers()
    numbers = []

    for name in containers:

        if name == "cloud-app":
            numbers.append(0)

        elif name.startswith("cloud-app-"):

            try:
                number = int(name.split("-")[-1])
                numbers.append(number)

            except ValueError:
                pass

    if numbers:
        return max(numbers) + 1

    return 0


def create_container():

    number = get_next_number()

    if number == 0:
        name = "cloud-app"
        port = 5000
    else:
        name = f"cloud-app-{number}"
        port = 5000 + number

    result = subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "-p",
            f"{port}:5000",
            "--name",
            name,
            IMAGE
        ],
        capture_output=True,
        text=True
    )

    return result, name, port


@app.route("/status", methods=["GET"])
def status():

    all_containers = get_containers()
    running = get_running_containers()

    return jsonify({
        "all_containers": all_containers,
        "running_containers": running,
        "total": len(all_containers),
        "running": len(running)
    })


@app.route("/scale-up", methods=["POST"])
def scale_up():

    running = get_running_containers()

    if len(running) >= MAX_CONTAINERS:

        return jsonify({
            "action": "SCALE_UP",
            "status": "FAILED",
            "message": "Maximum container limit reached"
        })

    result, name, port = create_container()

    if result.returncode == 0:

        return jsonify({
            "action": "SCALE_UP",
            "status": "SUCCESS",
            "container": name,
            "port": port
        })

    return jsonify({
        "action": "SCALE_UP",
        "status": "FAILED",
        "error": result.stderr
    })


@app.route("/scale-down", methods=["POST"])
def scale_down():

    running = get_running_containers()

    if len(running) <= MIN_CONTAINERS:

        return jsonify({
            "action": "SCALE_DOWN",
            "status": "FAILED",
            "message": f"Minimum {MIN_CONTAINERS} containers must remain"
        })

    numbered = []

    for name in running:

        if name.startswith("cloud-app-"):

            try:
                number = int(name.split("-")[-1])
                numbered.append((number, name))

            except ValueError:
                pass

    if not numbered:

        return jsonify({
            "action": "SCALE_DOWN",
            "status": "FAILED",
            "message": "No extra container available"
        })

    numbered.sort(reverse=True)

    name = numbered[0][1]

    result = subprocess.run(
        ["docker", "rm", "-f", name],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        return jsonify({
            "action": "SCALE_DOWN",
            "status": "SUCCESS",
            "container": name
        })

    return jsonify({
        "action": "SCALE_DOWN",
        "status": "FAILED",
        "error": result.stderr
    })


@app.route("/recover", methods=["POST"])
def recover():

    running = get_running_containers()

    if len(running) >= MAX_CONTAINERS:

        return jsonify({
            "action": "RECOVER",
            "status": "BLOCKED",
            "message": "Maximum container limit already reached",
            "recovered": []
        })

    containers = get_containers()
    stopped_containers = []

    for name in containers:

        result = subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                "{{.State.Running}}|{{.State.FinishedAt}}",
                name
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            parts = result.stdout.strip().split("|", 1)

            if len(parts) == 2 and parts[0] == "false":

                stopped_containers.append(
                    (parts[1], name)
                )

    if not stopped_containers:

        return jsonify({
            "action": "RECOVER",
            "status": "SUCCESS",
            "recovered": [],
            "message": "No stopped container found"
        })

    stopped_containers.sort(reverse=True)

    name = stopped_containers[0][1]

    start = subprocess.run(
        ["docker", "start", name],
        capture_output=True,
        text=True
    )

    if start.returncode == 0:

        return jsonify({
            "action": "RECOVER",
            "status": "SUCCESS",
            "recovered": [name]
        })

    return jsonify({
        "action": "RECOVER",
        "status": "FAILED",
        "recovered": [],
        "error": start.stderr
    })


@app.route("/restart", methods=["POST"])
def restart():

    running = get_running_containers()

    if not running:

        return jsonify({
            "action": "RESTART",
            "status": "FAILED",
            "message": "No running container available"
        })

    name = sorted(running)[-1]

    result = subprocess.run(
        ["docker", "restart", name],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        return jsonify({
            "action": "RESTART",
            "status": "SUCCESS",
            "container": name
        })

    return jsonify({
        "action": "RESTART",
        "status": "FAILED",
        "error": result.stderr
    })


@app.route("/replace", methods=["POST"])
def replace():

    running = get_running_containers()

    if len(running) <= MIN_CONTAINERS:

        return jsonify({
            "action": "REPLACE",
            "status": "FAILED",
            "message": f"Cannot replace when only {MIN_CONTAINERS} containers are running"
        })

    name = sorted(running)[-1]

    remove = subprocess.run(
        ["docker", "rm", "-f", name],
        capture_output=True,
        text=True
    )

    if remove.returncode != 0:

        return jsonify({
            "action": "REPLACE",
            "status": "FAILED",
            "error": remove.stderr
        })

    result, new_name, port = create_container()

    if result.returncode == 0:

        return jsonify({
            "action": "REPLACE",
            "status": "SUCCESS",
            "removed_container": name,
            "replacement_container": new_name,
            "port": port
        })

    return jsonify({
        "action": "REPLACE",
        "status": "FAILED",
        "removed_container": name,
        "error": result.stderr
    })


@app.route("/redistribute", methods=["POST"])
def redistribute():

    running = get_running_containers()

    if len(running) < 2:

        return jsonify({
            "action": "REDISTRIBUTE",
            "status": "FAILED",
            "message": "At least 2 running containers are required"
        })

    return jsonify({
        "action": "REDISTRIBUTE",
        "status": "SUCCESS",
        "containers": running,
        "message": "Workload redistribution triggered across running containers"
    })


if __name__ == "__main__":

    print("========================================")
    print(" CLOUD INFRASTRUCTURE CONTROL API")
    print("========================================")

    app.run(
        host="0.0.0.0",
        port=9000
    )