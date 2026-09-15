import subprocess
import time


def get_container_stats():

    result = subprocess.run(
        [
            "docker", "stats",
            "--no-stream",
            "--format",
            "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"
        ],
        capture_output=True,
        text=True
    )

    print("\nContainer Monitoring")
    print("--------------------")

    for line in result.stdout.splitlines():

        data = line.split("|")

        if len(data) == 3:

            name = data[0]
            cpu = data[1]
            memory = data[2]

            print(f"Container : {name}")
            print(f"CPU       : {cpu}")
            print(f"Memory    : {memory}")
            print("--------------------")


while True:

    get_container_stats()

    time.sleep(5)