def calculate_decision(
    current_cpu,
    predicted_cpu,
    memory,
    running_containers,
    healthy=True,
    cost_per_hour=0.05,
    energy_per_container=50
):
    """
    Decision Intelligence model.

    Considers:
    - Performance
    - Reliability
    - Cost
    - Energy
    """

    # --------------------------------------------------
    # 1. Calculate current cost and energy
    # --------------------------------------------------

    current_cost = running_containers * cost_per_hour
    current_energy = running_containers * energy_per_container

    # --------------------------------------------------
    # 2. Reliability
    # --------------------------------------------------

    if not healthy:
        return {
            "decision": "RECOVER",
            "reason": "Infrastructure resource is unhealthy",
            "weighted_score": 0,
            "scores": {
                "performance": 0,
                "reliability": 0,
                "cost": 0,
                "energy": 0
            },
            "metrics": {
                "current_cpu": current_cpu,
                "predicted_cpu": predicted_cpu,
                "memory": memory,
                "running_containers": running_containers,
                "current_cost_per_hour": round(current_cost, 4),
                "current_energy_watts": current_energy
            }
        }

    reliability_score = 100

    # --------------------------------------------------
    # 3. Performance Score
    # --------------------------------------------------

    if predicted_cpu >= 90:
        performance_score = 100
    elif predicted_cpu >= 80:
        performance_score = 80
    elif predicted_cpu >= 60:
        performance_score = 60
    elif predicted_cpu >= 30:
        performance_score = 40
    else:
        performance_score = 20

    # --------------------------------------------------
    # 4. Cost Score
    # --------------------------------------------------

    if current_cost <= 0.10:
        cost_score = 100
    elif current_cost <= 0.20:
        cost_score = 80
    elif current_cost <= 0.30:
        cost_score = 60
    else:
        cost_score = 40

    # --------------------------------------------------
    # 5. Energy Score
    # --------------------------------------------------

    if current_energy <= 100:
        energy_score = 100
    elif current_energy <= 200:
        energy_score = 80
    elif current_energy <= 300:
        energy_score = 60
    else:
        energy_score = 40

    # --------------------------------------------------
    # 6. Weighted Decision Score
    # --------------------------------------------------

    weighted_score = (
        performance_score * 0.40
        + reliability_score * 0.30
        + cost_score * 0.15
        + energy_score * 0.15
    )

    # --------------------------------------------------
    # 7. Decision Rules
    # --------------------------------------------------

    if predicted_cpu > 80:
        decision = "SCALE_UP"
        reason = "Predicted workload is high"

    elif predicted_cpu < 30 and running_containers > 2:
        decision = "SCALE_DOWN"
        reason = "Predicted workload is low"

    else:
        decision = "NO_ACTION"
        reason = "Infrastructure is within acceptable limits"

    # --------------------------------------------------
    # 8. Return complete result
    # --------------------------------------------------

    return {
        "decision": decision,
        "reason": reason,
        "weighted_score": round(weighted_score, 2),
        "scores": {
            "performance": performance_score,
            "reliability": reliability_score,
            "cost": cost_score,
            "energy": energy_score
        },
        "metrics": {
            "current_cpu": current_cpu,
            "predicted_cpu": predicted_cpu,
            "memory": memory,
            "running_containers": running_containers,
            "current_cost_per_hour": round(current_cost, 4),
            "current_energy_watts": current_energy
        }
    }


if __name__ == "__main__":

    result = calculate_decision(
        current_cpu=70,
        predicted_cpu=90,
        memory=65,
        running_containers=2,
        healthy=True
    )

    print("Decision Intelligence Result")
    print("============================")
    print(result)