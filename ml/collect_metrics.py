import subprocess
import csv
import time
from datetime import datetime
from pathlib import Path


OUTPUT_FILE = Path(
    "ml/data/real_workload_metrics_v3.csv"
)

INTERVAL = 5


def get_container_stats():

    result = subprocess.run(
        [
            "docker",
            "stats",
            "--no-stream",
            "--format",
            "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}|{{.NetIO}}"
        ],
        capture_output=True,
        text=True,
        check=True
    )

    containers = []

    for line in result.stdout.strip().splitlines():

        parts = line.split("|")

        if len(parts) != 4:
            continue

        name, cpu, memory, network = parts

        cpu_value = float(
            cpu.replace("%", "")
        )

        memory_used = (
            memory
            .split("/")[0]
            .strip()
        )

        if memory_used.endswith("MiB"):

            memory_value = float(
                memory_used
                .replace("MiB", "")
                .strip()
            )

        elif memory_used.endswith("GiB"):

            memory_value = (
                float(
                    memory_used
                    .replace("GiB", "")
                    .strip()
                )
                * 1024
            )

        else:

            memory_value = 0.0

        net_parts = network.split("/")

        network_rx = net_parts[0].strip()
        network_tx = net_parts[1].strip()

        containers.append({

            "container_name":
                name,

            "cpu_percent":
                cpu_value,

            "memory_used_mib":
                memory_value,

            "network_rx":
                network_rx,

            "network_tx":
                network_tx
        })

    return containers


def main():

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline=""
    ) as file:

        fieldnames = [
            "timestamp",
            "container_name",
            "cpu_percent",
            "memory_used_mib",
            "network_rx",
            "network_tx",
            "resource_count"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        print(
            "REAL DOCKER METRICS COLLECTOR V3"
        )

        print(
            "================================="
        )

        print(
            f"Saving data to: {OUTPUT_FILE}"
        )

        print(
            f"Collection interval: "
            f"{INTERVAL} seconds"
        )

        print(
            "Press Ctrl+C to stop.\n"
        )

        try:

            while True:

                containers = (
                    get_container_stats()
                )

                resource_count = (
                    len(containers)
                )

                timestamp = (
                    datetime.now()
                    .isoformat()
                )

                for container in containers:

                    writer.writerow({

                        "timestamp":
                            timestamp,

                        "container_name":
                            container[
                                "container_name"
                            ],

                        "cpu_percent":
                            container[
                                "cpu_percent"
                            ],

                        "memory_used_mib":
                            container[
                                "memory_used_mib"
                            ],

                        "network_rx":
                            container[
                                "network_rx"
                            ],

                        "network_tx":
                            container[
                                "network_tx"
                            ],

                        "resource_count":
                            resource_count
                    })

                file.flush()

                print(
                    f"[{timestamp}] "
                    f"Resources: "
                    f"{resource_count}"
                )

                for container in containers:

                    print(
                        f"  "
                        f"{container['container_name']} "
                        f"| CPU: "
                        f"{container['cpu_percent']:.2f}% "
                        f"| Memory: "
                        f"{container['memory_used_mib']:.2f} MiB"
                    )

                print()

                time.sleep(
                    INTERVAL
                )

        except KeyboardInterrupt:

            print(
                "\nCollector stopped."
            )


if __name__ == "__main__":

    main()