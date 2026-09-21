from .infrastructure_client import (
    get_status,
    scale_up,
    scale_down,
    recover
)

from .decision_model import calculate_decision


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


# Get current infrastructure status
status = get_status()
running_containers = status["running"]

print("Current infrastructure:")
print(status)


# Simulated prediction from Member 2
predicted_cpu = 90


# Use Decision Model
decision_result = calculate_decision(
    current_cpu=70,
    predicted_cpu=predicted_cpu,
    memory=65,
    running_containers=running_containers,
    healthy=True
)

decision = decision_result["decision"]
reason = decision_result["reason"]


print("\nPredicted CPU:", predicted_cpu)
print("Decision:", decision)
print("Reason:", reason)


# Execute the decision
result = execute_decision(decision)

print("\nExecution result:")
print(result)