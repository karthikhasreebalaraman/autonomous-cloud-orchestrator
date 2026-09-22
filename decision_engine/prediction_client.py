from pathlib import Path
import sys

# Allow importing from the ml folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ml.predict_service import WorkloadPredictor


predictor = WorkloadPredictor()


def get_prediction(
    current_cpu,
    memory,
    request_rate,
    network,
    latency,
    resource_count,

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
):
    """
    Get future CPU prediction from Member 2 ML model.
    """

    predicted_cpu = predictor.predict(
        cpu=current_cpu,
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

    return {
        "current_cpu": current_cpu,
        "memory": memory,
        "request_rate": request_rate,
        "predicted_cpu": predicted_cpu
    }


if __name__ == "__main__":

    result = get_prediction(

        current_cpu=60,
        memory=55,
        request_rate=200,
        network=17,
        latency=28,
        resource_count=2,

        cpu_lag_1=57,
        cpu_lag_2=54,
        cpu_lag_3=52,

        request_lag_1=190,
        request_lag_2=175,
        request_lag_3=160,

        cpu_rolling_mean_3=57,
        request_rolling_mean_3=188,

        cpu_change=3,
        request_change=10
    )

    print()
    print("=" * 60)
    print("MEMBER 2 → MEMBER 3 PREDICTION")
    print("=" * 60)

    print(f"Current CPU    : {result['current_cpu']}%")
    print(f"Memory         : {result['memory']}%")
    print(f"Request Rate   : {result['request_rate']} req/s")
    print(f"Predicted CPU  : {result['predicted_cpu']}%")

    print("=" * 60)