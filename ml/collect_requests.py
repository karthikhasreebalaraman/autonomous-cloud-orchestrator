import csv
import time
import requests
from datetime import datetime
from pathlib import Path


URL = "http://localhost:5000/cpu"
OUTPUT_FILE = Path("ml/data/request_metrics_v2.csv")

REQUEST_INTERVAL = 0.2


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = OUTPUT_FILE.exists()

    with open(OUTPUT_FILE, "a", newline="") as file:
        fieldnames = [
            "timestamp",
            "request_number",
            "status_code",
            "latency_ms"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        print("Request & Latency Collector")
        print("===========================")
        print(f"Target: {URL}")
        print(f"Request interval: {REQUEST_INTERVAL} seconds")
        print(f"Saving to: {OUTPUT_FILE}")
        print("Press Ctrl+C to stop.\n")

        request_number = 0

        try:
            while True:
                request_number += 1
                timestamp = datetime.now().isoformat()

                start = time.perf_counter()

                try:
                    response = requests.get(URL, timeout=10)

                    end = time.perf_counter()

                    latency_ms = (end - start) * 1000

                    writer.writerow({
                        "timestamp": timestamp,
                        "request_number": request_number,
                        "status_code": response.status_code,
                        "latency_ms": round(latency_ms, 3)
                    })

                    file.flush()

                    print(
                        f"[{timestamp}] "
                        f"Request: {request_number} | "
                        f"Status: {response.status_code} | "
                        f"Latency: {latency_ms:.2f} ms"
                    )

                except requests.RequestException as e:
                    print(
                        f"[{timestamp}] "
                        f"Request: {request_number} | "
                        f"ERROR: {e}"
                    )

                time.sleep(REQUEST_INTERVAL)

        except KeyboardInterrupt:
            print("\nRequest collector stopped.")


if __name__ == "__main__":
    main()