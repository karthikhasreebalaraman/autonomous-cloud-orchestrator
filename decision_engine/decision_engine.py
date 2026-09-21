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

from .prediction_client import get_prediction


def execute_decision(decision):
    """Execute the selected infrastructure action."""

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
# 2. Current cost and energy
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
# 3. Scaling cost/energy comparison
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
# 4. Get prediction
# --------------------------------------------------

current_cpu = 50
memory = 65

prediction = get_prediction(
    current_cpu=current_cpu,
    memory=memory,
    predicted_cpu=50
)
predicted_cpu = prediction["predicted_cpu"]

print("\n========================================")
print(" PREDICTION")
print("========================================")

print("Current CPU:", current_cpu)
print("Memory:", memory)
print("Predicted CPU:", predicted_cpu)


# --------------------------------------------------
# 5. Decision Intelligence
# --------------------------------------------------

decision_result = calculate_decision(
    current_cpu=current_cpu,
    predicted_cpu=predicted_cpu,
    memory=memory,
    running_containers=running_containers,
    healthy=True
)

decision = decision_result["decision"]
reason = decision_result["reason"]


print("\n========================================")
print(" DECISION INTELLIGENCE")
print("========================================")

print("Decision:", decision)
print("Reason:", reason)

print("\nWeighted Score:",
      decision_result["weighted_score"])

print("\nIndividual Scores:")

scores = decision_result["scores"]

print("Performance:", scores["performance"])
print("Reliability:", scores["reliability"])
print("Cost:", scores["cost"])
print("Energy:", scores["energy"])


# --------------------------------------------------
# 6. Execute decision
# --------------------------------------------------

result = execute_decision(decision)

print("\n========================================")
print(" EXECUTION RESULT")
print("========================================")

print(result)