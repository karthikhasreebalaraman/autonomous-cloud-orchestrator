import subprocess
import time


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


def is_running(name):

    result = subprocess.run(
        [
            "docker",
            "inspect",
            "-f",
            "{{.State.Running}}",
            name
        ],
        capture_output=True,
        text=True
    )

    return result.returncode == 0 and result.stdout.strip() == "true"


def recover_container(name):

    print(f"FAILURE DETECTED: {name}")
    print(f"Attempting recovery of {name}...")

    result = subprocess.run(
        ["docker", "start", name],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"RECOVERY SUCCESSFUL: {name}")
    else:
        print(f"RECOVERY FAILED: {name}")
        print(result.stderr)


print("========================================")
print(" CLOUD FAULT RECOVERY MONITOR")
print("========================================")

while True:

    containers = get_containers()

    print("\nChecking container health...")
    print("--------------------------------")

    for name in containers:

        if is_running(name):
            print(f"{name}: HEALTHY")

        else:
            recover_container(name)

    print(f"Containers detected: {len(containers)}")

    time.sleep(10)