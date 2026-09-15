import subprocess


IMAGE = "cloud-orchestrator-app"


def scale_up():

    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )

    names = result.stdout.splitlines()

    numbers = []

    for name in names:
        if name.startswith("cloud-app-"):
            try:
                number = int(name.split("-")[-1])
                numbers.append(number)
            except ValueError:
                pass

    if numbers:
        number = max(numbers) + 1
    else:
        number = 2

    name = f"cloud-app-{number}"
    port = 5000 + number

    subprocess.run([
        "docker", "run",
        "-d",
        "-p", f"{port}:5000",
        "--name", name,
        IMAGE
    ])

    print(f"Scaled UP: {name}")
    print(f"Running on port {port}")


def scale_down():

    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )

    names = result.stdout.splitlines()

    containers = []

    for name in names:
        if name.startswith("cloud-app-"):
            try:
                number = int(name.split("-")[-1])
                containers.append((number, name))
            except ValueError:
                pass

    if not containers:
        print("No extra containers to remove.")
        return

    containers.sort(reverse=True)

    name = containers[0][1]

    subprocess.run(["docker", "rm", "-f", name])

    print(f"Scaled DOWN: {name}")


print("Cloud Infrastructure Auto Scaler")
print("----------------------------------")
print("1. Scale UP")
print("2. Scale DOWN")
print("3. Exit")

choice = input("Enter your choice: ")

if choice == "1":
    scale_up()

elif choice == "2":
    scale_down()

elif choice == "3":
    print("Exiting...")

else:
    print("Invalid choice.")