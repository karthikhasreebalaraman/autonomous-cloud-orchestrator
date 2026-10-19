from .prediction_client import get_prediction
from .decision_model import calculate_decision
from .infrastructure_client import (
    get_status,
    scale_up,
    scale_down,
    recover,
    restart,
    replace,
    redistribute
)


def execute_decision(decision):

    if decision == "SCALE_UP":
        return scale_up()

    elif decision == "SCALE_DOWN":
        return scale_down()

    elif decision == "RECOVER":
        return recover()

    elif decision == "RESTART":
        return restart()

    elif decision == "REPLACE":
        return replace()

    elif decision == "REDISTRIBUTE":
        return redistribute()

    else:
        return {
            "action": "NO_ACTION",
            "status": "SUCCESS",
            "message": "No infrastructure action required"
        }


def run_decision_engine():

    print("=" * 70)
    print("AUTONOMOUS CLOUD ORCHESTRATOR")
    print("=" * 70)

    print("\nINFRASTRUCTURE INITIALIZATION")
    print("-" * 30)

    infrastructure = get_status()

    print(f"Required Containers : 2")
    print(f"Running Containers  : {infrastructure['running']}")

    print("\nCURRENT INFRASTRUCTURE")
    print("-" * 30)

    print(f"Running Containers : {infrastructure['running']}")
    print(f"Containers         : {infrastructure['running_containers']}")

    current_cpu = 85
    memory = 75
    request_rate = 500
    network = 30
    latency = 45

    cpu_lag_1 = 80
    cpu_lag_2 = 75
    cpu_lag_3 = 70

    request_lag_1 = 450
    request_lag_2 = 400
    request_lag_3 = 350

    cpu_rolling_mean_3 = 75
    request_rolling_mean_3 = 400

    cpu_change = 5
    request_change = 50

    print("\nCURRENT WORKLOAD")
    print("-" * 30)

    print(f"CPU            : {current_cpu}%")
    print(f"Memory         : {memory}%")
    print(f"Request Rate   : {request_rate} req/s")
    print(f"Network        : {network}")
    print(f"Latency        : {latency} ms")

    prediction = get_prediction(
        current_cpu,
        memory,
        request_rate,
        network,
        latency,
        infrastructure["running"],
        cpu_lag_1,
        cpu_lag_2,
        cpu_lag_3,
        request_lag_1,
        request_lag_2,
        request_lag_3,
        cpu_rolling_mean_3,
        request_rolling_mean_3,
        cpu_change,
        request_change
    )

    print("\nML PREDICTION")
    print("-" * 30)

    print(f"Predicted CPU (+5 min): {prediction['predicted_cpu']}%")

    decision_result = calculate_decision(
        current_cpu=current_cpu,
        predicted_cpu=prediction["predicted_cpu"],
        memory=memory,
        running_containers=infrastructure["running"],
        healthy=True
    )

    decision = decision_result["decision"]

    print("\nDECISION INTELLIGENCE")
    print("-" * 30)

    print(f"Decision       : {decision}")
    print(f"Reason         : {decision_result['reason']}")
    print(f"Weighted Score : {decision_result['weighted_score']}")

    print("\nSCORES")
    print("-" * 30)

    print(f"Performance : {decision_result['scores']['performance']}")
    print(f"Reliability : {decision_result['scores']['reliability']}")
    print(f"Cost        : {decision_result['scores']['cost']}")
    print(f"Energy      : {decision_result['scores']['energy']}")

    print("\nEXECUTION RESULT")
    print("-" * 30)

    execution = execute_decision(decision)

    print(execution)

    final_infrastructure = get_status()

    print("\nFINAL INFRASTRUCTURE")
    print("-" * 30)

    print(f"Running Containers : {final_infrastructure['running']}")
    print(f"Containers         : {final_infrastructure['running_containers']}")

    print("\n" + "=" * 70)
    print("DECISION ENGINE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    run_decision_engine()