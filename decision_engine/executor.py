import requests


CONTROL_API = "http://localhost:9000"


def execute_decision(decision):

    print("\nEXECUTION")
    print("---------")

    if decision == "SCALE_UP":

        print("Executing SCALE_UP...")

        response = requests.post(
            f"{CONTROL_API}/scale-up",
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        print(f"Action    : {result.get('action')}")
        print(f"Container : {result.get('container')}")
        print(f"Port      : {result.get('port')}")
        print(f"Status    : {result.get('status')}")

        return result

    elif decision == "SCALE_DOWN":

        print("Executing SCALE_DOWN...")

        response = requests.post(
            f"{CONTROL_API}/scale-down",
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        print(f"Action    : {result.get('action')}")
        print(f"Container : {result.get('container')}")
        print(f"Status    : {result.get('status')}")

        return result

    elif decision == "RECOVER":

        print("Executing RECOVER...")

        response = requests.post(
            f"{CONTROL_API}/recover",
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        print(f"Action : {result.get('action')}")
        print(f"Status : {result.get('status')}")

        return result

    else:

        print("No infrastructure action required.")

        return {
            "action": "NO_ACTION",
            "status": "SKIPPED"
        }


if __name__ == "__main__":

    print("Executor module loaded successfully.")

    result = execute_decision("NO_ACTION")

    print(result)
