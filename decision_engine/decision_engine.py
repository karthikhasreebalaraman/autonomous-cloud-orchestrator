from .infrastructure_client import (
    get_status,
    scale_up,
    scale_down,
    recover
)


def decide(predicted_cpu, running_containers, unhealthy=False):

    if unhealthy:
        return "RECOVER"

    if predicted_cpu > 80:
        return "SCALE_UP"

    if predicted_cpu < 30 and running_containers > 2:
        return "SCALE_DOWN"

    return "NO_ACTION"


def execute_decision(decision):

    if decision == "SCALE_UP":
        return scale_up()

    if decision == "SCALE_DOWN":
        return scale_down()

    if decision == "RECOVER":
        return recover()

    return {
        "action": "NO_ACTION",
        "status": "NO_EXECUTION"
    }


# -----------------------------
# TEST
# -----------------------------

status = get_status()

running_containers = status["running"]

print("Current infrastructure:")
print(status)

# Simulated prediction from Member 2
predicted_cpu = 90

decision = decide(
    predicted_cpu=predicted_cpu,
    running_containers=running_containers,
    unhealthy=False
)

print("\nPredicted CPU:", predicted_cpu)
print("Decision:", decision)

result = execute_decision(decision)

print("Execution result:")
print(result)