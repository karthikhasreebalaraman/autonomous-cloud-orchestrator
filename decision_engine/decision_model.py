def calculate_decision(
    current_cpu,
    predicted_cpu,
    memory,
    running_containers,
    healthy=True
):
    """
    Decide what infrastructure action should be taken
    based on the current and predicted system state.
    """

    # 1. Handle unhealthy infrastructure first
    if not healthy:
        return {
            "decision": "RECOVER",
            "reason": "Infrastructure resource is unhealthy"
        }

    # 2. Predicted overload
    if predicted_cpu > 80:
        return {
            "decision": "SCALE_UP",
            "reason": f"Predicted CPU is high: {predicted_cpu}%"
        }

    # 3. Low workload
    if predicted_cpu < 30 and running_containers > 2:
        return {
            "decision": "SCALE_DOWN",
            "reason": f"Predicted CPU is low: {predicted_cpu}%"
        }

    # 4. Otherwise, maintain current infrastructure
    return {
        "decision": "NO_ACTION",
        "reason": "Current and predicted workload are within safe limits"
    }


# -----------------------------
# TESTING
# -----------------------------

if __name__ == "__main__":

    result = calculate_decision(
        current_cpu=70,
        predicted_cpu=90,
        memory=65,
        running_containers=2,
        healthy=True
    )

    print("Decision Result:")
    print(result)