from prediction_client import get_prediction
from decision_model import calculate_decision


def run_decision_engine():

    # =================================================
    # CURRENT WORKLOAD
    # =================================================

    current_cpu = 60
    memory = 55
    request_rate = 200
    network = 17
    latency = 28
    resource_count = 2

    # =================================================
    # HISTORICAL WORKLOAD
    # =================================================

    cpu_lag_1 = 57
    cpu_lag_2 = 54
    cpu_lag_3 = 52

    request_lag_1 = 190
    request_lag_2 = 175
    request_lag_3 = 160

    cpu_rolling_mean_3 = 57
    request_rolling_mean_3 = 188

    cpu_change = 3
    request_change = 10

    # =================================================
    # MEMBER 2 → ML PREDICTION
    # =================================================

    prediction = get_prediction(

        current_cpu=current_cpu,
        memory=memory,
        request_rate=request_rate,
        network=network,
        latency=latency,
        resource_count=resource_count,

        cpu_lag_1=cpu_lag_1,
        cpu_lag_2=cpu_lag_2,
        cpu_lag_3=cpu_lag_3,

        request_lag_1=request_lag_1,
        request_lag_2=request_lag_2,
        request_lag_3=request_lag_3,

        cpu_rolling_mean_3=cpu_rolling_mean_3,
        request_rolling_mean_3=request_rolling_mean_3,

        cpu_change=cpu_change,
        request_change=request_change
    )

    predicted_cpu = prediction["predicted_cpu"]

    # =================================================
    # DISPLAY CURRENT STATE
    # =================================================

    print()
    print("=" * 70)
    print("AUTONOMOUS CLOUD ORCHESTRATOR")
    print("=" * 70)

    print("\nCURRENT WORKLOAD")
    print("----------------")
    print(f"CPU            : {current_cpu}%")
    print(f"Memory         : {memory}%")
    print(f"Request Rate   : {request_rate} req/s")
    print(f"Network        : {network}")
    print(f"Latency        : {latency} ms")
    print(f"Containers     : {resource_count}")

    # =================================================
    # DISPLAY ML PREDICTION
    # =================================================

    print("\nML PREDICTION")
    print("-------------")
    print(
        f"Predicted CPU (+5 min): {predicted_cpu}%"
    )

    # =================================================
    # MEMBER 3 → DECISION INTELLIGENCE
    # =================================================

    decision_result = calculate_decision(

        current_cpu=current_cpu,

        predicted_cpu=predicted_cpu,

        memory=memory,

        running_containers=resource_count,

        healthy=True
    )

    # =================================================
    # DISPLAY DECISION
    # =================================================

    print("\nDECISION INTELLIGENCE")
    print("---------------------")

    print(
        f"Decision       : "
        f"{decision_result['decision']}"
    )

    print(
        f"Reason         : "
        f"{decision_result['reason']}"
    )

    print(
        f"Weighted Score : "
        f"{decision_result['weighted_score']}"
    )

    print("\nSCORES")
    print("------")

    print(
        f"Performance : "
        f"{decision_result['scores']['performance']}"
    )

    print(
        f"Reliability : "
        f"{decision_result['scores']['reliability']}"
    )

    print(
        f"Cost        : "
        f"{decision_result['scores']['cost']}"
    )

    print(
        f"Energy      : "
        f"{decision_result['scores']['energy']}"
    )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_decision_engine()