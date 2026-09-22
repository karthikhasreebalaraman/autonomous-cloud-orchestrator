import csv
import requests
import threading
import time
from datetime import datetime
from pathlib import Path


URL = "http://localhost:5000/cpu"

OUTPUT_FILE = Path(
    "ml/data/request_metrics_v3.csv"
)


# --------------------------------------------------
# WORKLOAD PLAN
# --------------------------------------------------

# (phase name, requests per second, duration seconds)

PHASES = [
    ("NO LOAD", 0, 30),

    ("LOW LOAD", 2, 60),

    ("MEDIUM LOAD", 5, 60),

    ("HIGH LOAD", 10, 60),

    ("RECOVERY", 0, 30),

    ("LOW LOAD", 2, 60),

    ("HIGH LOAD", 10, 60),

    ("RECOVERY", 0, 30),

    ("MEDIUM LOAD", 5, 60),

    ("HIGH LOAD", 10, 60),

    ("RECOVERY", 0, 30),

    ("LOW LOAD", 2, 60),

    ("MEDIUM LOAD", 5, 60),

    ("HIGH LOAD", 10, 60),

    ("RECOVERY", 0, 30),
]


# --------------------------------------------------
# REQUEST WORKER
# --------------------------------------------------

def worker(
    stop_event,
    interval,
    writer,
    file,
    counter,
    lock
):

    while not stop_event.is_set():

        start = time.perf_counter()

        try:

            response = requests.get(
                URL,
                timeout=10
            )

            end = time.perf_counter()

            latency_ms = (
                end - start
            ) * 1000

            with lock:

                counter[0] += 1

                writer.writerow({
                    "timestamp":
                        datetime.now().isoformat(),

                    "request_number":
                        counter[0],

                    "status_code":
                        response.status_code,

                    "latency_ms":
                        round(
                            latency_ms,
                            3
                        )
                })

                file.flush()

                print(
                    f"[{datetime.now().strftime('%H:%M:%S')}] "
                    f"Request: {counter[0]} | "
                    f"Status: {response.status_code} | "
                    f"Latency: {latency_ms:.1f} ms"
                )

        except requests.RequestException:

            pass

        elapsed = (
            time.perf_counter()
            - start
        )

        remaining = max(
            0,
            interval - elapsed
        )

        stop_event.wait(
            remaining
        )


# --------------------------------------------------
# RUN ONE PHASE
# --------------------------------------------------

def run_phase(
    name,
    requests_per_second,
    duration,
    writer,
    file
):

    print()
    print("=" * 65)
    print(f"PHASE: {name}")
    print(
        f"Target request rate: "
        f"{requests_per_second} req/s"
    )
    print(
        f"Duration: {duration} seconds"
    )
    print("=" * 65)

    # No workload
    if requests_per_second == 0:

        time.sleep(duration)

        return

    workers = min(
        requests_per_second,
        10
    )

    interval = (
        workers /
        requests_per_second
    )

    stop_event = threading.Event()

    counter = [0]

    lock = threading.Lock()

    threads = []

    for _ in range(workers):

        thread = threading.Thread(
            target=worker,
            args=(
                stop_event,
                interval,
                writer,
                file,
                counter,
                lock
            ),
            daemon=True
        )

        thread.start()

        threads.append(thread)

    time.sleep(duration)

    stop_event.set()

    for thread in threads:

        thread.join(
            timeout=2
        )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

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
            "request_number",
            "status_code",
            "latency_ms"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        print()
        print(
            "LONG REAL WORKLOAD EXPERIMENT V3"
        )
        print(
            "================================="
        )
        print(
            f"Target: {URL}"
        )
        print(
            f"Output: {OUTPUT_FILE}"
        )

        total_duration = sum(
            phase[2]
            for phase in PHASES
        )

        print(
            f"Total duration: "
            f"{total_duration // 60} minutes "
            f"{total_duration % 60} seconds"
        )

        print()

        for (
            name,
            rate,
            duration
        ) in PHASES:

            run_phase(
                name,
                rate,
                duration,
                writer,
                file
            )

    print()
    print("=" * 65)
    print("EXPERIMENT COMPLETED")
    print("=" * 65)


if __name__ == "__main__":

    main()