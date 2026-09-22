import pandas as pd
import joblib

MODEL_FILE = "ml/models/best_model.pkl"

# Load trained model
model = joblib.load(MODEL_FILE)

# Exact feature order used during training
FEATURES = [
    "cpu",
    "memory",
    "request_rate",
    "network",
    "latency",
    "resource_count",
    "cpu_lag_1",
    "cpu_lag_2",
    "cpu_lag_3",
    "request_lag_1",
    "request_lag_2",
    "request_lag_3",
    "cpu_rolling_mean_3",
    "request_rolling_mean_3",
    "cpu_change",
    "request_change"
]


def predict_future_cpu(
    cpu,
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
    Predict CPU utilization 5 minutes into the future.
    """

    input_data = pd.DataFrame([{
        "cpu": cpu,
        "memory": memory,
        "request_rate": request_rate,
        "network": network,
        "latency": latency,
        "resource_count": resource_count,
        "cpu_lag_1": cpu_lag_1,
        "cpu_lag_2": cpu_lag_2,
        "cpu_lag_3": cpu_lag_3,
        "request_lag_1": request_lag_1,
        "request_lag_2": request_lag_2,
        "request_lag_3": request_lag_3,
        "cpu_rolling_mean_3": cpu_rolling_mean_3,
        "request_rolling_mean_3": request_rolling_mean_3,
        "cpu_change": cpu_change,
        "request_change": request_change
    }])

    prediction = model.predict(input_data[FEATURES])[0]

    return float(prediction)


# --------------------------------------------------
# TEST PREDICTION
# --------------------------------------------------

if __name__ == "__main__":

    # Example current workload
    prediction = predict_future_cpu(
        cpu=60,
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

    print("========================================")
    print(" MEMBER 2 - CPU PREDICTION")
    print("========================================")

    print(f"Current CPU        : 60%")
    print(f"Current Requests   : 200 req/min")
    print(f"Predicted CPU +5m  : {prediction:.2f}%")

    print("========================================")