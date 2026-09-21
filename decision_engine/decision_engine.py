from .infrastructure_client import (
    get_status,
    scale_up,
    scale_down,
    recover
)

from .decision_model import calculate_decision

from .cost_energy_model import (
    calculate_cost_and_energy,
    compare_scaling_options
)


def execute_decision(decision):
    """
    Execute the infrastructure action selected
    by the Decision Model.
    """

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


# --------------------------------------------------
# 1. Get current infrastructure status
# --------------------------------------------------

status = get_status()
running_containers = status["running"]

print("========================================")
print(" CURRENT INFRASTRUCTURE")
print("========================================")
print(status)


# --------------------------------------------------
# 2. Calculate current cost and energy
# --------------------------------------------------

cost_energy = calculate_cost_and_energy(running_containers)

print("\n========================================")
print(" CURRENT COST AND ENERGY")
print("========================================")

print("Running containers:",
      cost_energy["running_containers"])

print("Estimated cost per hour: $",
      cost_energy["estimated_cost_per_hour"])

print("Estimated energy:",
      cost_energy["estimated_energy_watts"],
      "W")


# --------------------------------------------------
# 3. Compare scaling options
# --------------------------------------------------

scaling_options = compare_scaling_options(
    running_containers
)

print("\n========================================")
print(" SCALING COST/ENERGY COMPARISON")
print("========================================")

print("Current:")
print(scaling_options["current"])

print("\nScale Up:")
print(scaling_options["scale_up"])

print("\nScale Down:")
print(scaling_options["scale_down"])


# --------------------------------------------------
# 4. Simulated prediction from Member 2
# --------------------------------------------------

predicted_cpu = 90


# --------------------------------------------------
# 5. Decision Model
# --------------------------------------------------

decision_result = calculate_decision(
    current_cpu=70,
    predicted_cpu=predicted_cpu,
    memory=65,
    running_containers=running_containers,
    healthy=True
)

decision = decision_result["decision"]
reason = decision_result["reason"]


print("\n========================================")
print(" DECISION")
print("========================================")

print("Predicted CPU:", predicted_cpu)
print("Decision:", decision)
print("Reason:", reason)


# --------------------------------------------------
# 6. Execute the decision
# --------------------------------------------------

result = execute_decision(decision)

print("\n========================================")
print(" EXECUTION RESULT")
print("========================================")

print(result)