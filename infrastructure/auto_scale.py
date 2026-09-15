import subprocess
import time

MIN_CONTAINERS = 2
MAX_CONTAINERS = 6

SCALE_UP_THRESHOLD = 20.0
SCALE_DOWN_THRESHOLD = 5.0

COOLDOWN = 30


def get_containers():
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )

    names = []

    for name in result.stdout.splitlines():
        if name.startswith("cloud-app"):
            names.append(name)

    return names


def get_cpu():
    result = subprocess.run(
        [
            "docker",
            "stats",
            "--no-stream",
            "--format",
            "{{.Name}}|{{.CPUPerc}}"
        ],
        capture_output=True,
        text=True
    )

    total_cpu = 0
    count = 0

    print("\nChecking infrastructure...")
    print("--------------------------------")

    for line in result.stdout.splitlines():

        data = line.split("|")

        if len(data) == 2:

            name = data[0]
            cpu_text = data[1].replace("%", "")

            try:
                cpu = float(cpu_text)

                if name.startswith("cloud-app"):
                    print(f"{name}: {cpu:.2f}%")
                    total_cpu += cpu
                    count += 1

            except ValueError:
                pass

    return total_cpu, count


def scale_up():

    containers = get_containers()

    if len(containers) >= MAX_CONTAINERS:
        print("Maximum container limit reached.")
        return

    numbers = []

    for name in containers:

        if name == "cloud-app":
            numbers.append(1)

        elif name.startswith("cloud-app-"):

            try:
                number = int(name.split("-")[-1])
                numbers.append(number)

            except ValueError:
                pass

    number = max(numbers) + 1

    name = f"cloud-app-{number}"
    port = 5000 + number

    subprocess.run([
        "docker",
        "run",
        "-d",
        "-p",
        f"{port}:5000",
        "--name",
        name,
        "cloud-orchestrator-app"
    ])

    print(f"Scaled UP: {name}")
    print(f"Running on port {port}")


def scale_down():

    containers = get_containers()

    if len(containers) <= MIN_CONTAINERS:

        print(
            f"Minimum container limit reached "
            f"({MIN_CONTAINERS})."
        )

        return

    numbered = []

    for name in containers:

        if name.startswith("cloud-app-"):

            try:
                number = int(name.split("-")[-1])
                numbered.append((number, name))

            except ValueError:
                pass

    if numbered:

        numbered.sort(reverse=True)

        name = numbered[0][1]

        subprocess.run([
            "docker",
            "rm",
            "-f",
            name
        ])

        print(f"Scaled DOWN: {name}")


print("========================================")
print(" AUTONOMOUS CLOUD INFRASTRUCTURE")
print("        ORCHESTRATOR")
print("========================================")

last_action = 0

while True:

    total_cpu, active = get_cpu()

    if active > 0:
        average_cpu = total_cpu / active
    else:
        average_cpu = 0

    print(f"Active containers: {active}")
    print(f"Average CPU: {average_cpu:.2f}%")

    current_time = time.time()

    if current_time - last_action < COOLDOWN:

        print("Scaling cooldown active.")

    elif average_cpu > SCALE_UP_THRESHOLD:

        print("\nHIGH CPU DETECTED")
        print("Scaling UP...")

        scale_up()

        last_action = current_time

    elif average_cpu < SCALE_DOWN_THRESHOLD:

        if active > MIN_CONTAINERS:

            print("\nLOW CPU DETECTED")
            print("Scaling DOWN...")

            scale_down()

            last_action = current_time

        else:

            print(
                f"CPU is low, but minimum "
                f"{MIN_CONTAINERS} containers must remain."
            )

    else:

        print("No scaling action required.")

    time.sleep(15)