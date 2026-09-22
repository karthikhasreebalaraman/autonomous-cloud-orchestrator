import joblib
import pandas as pd
from pathlib import Path


MODEL_FILE = Path("ml/models/best_model.pkl")


class WorkloadPredictor:

    def __init__(self):

        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"Model not found: {MODEL_FILE}"
            )

        self.model = joblib.load(MODEL_FILE)

        self.features = [
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

    def predict(
        self,
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

        data = pd.DataFrame([{
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

        prediction = self.model.predict(
            data[self.features]
        )[0]

        prediction = max(
            0,
            min(100, float(prediction))
        )

        return round(prediction, 2)


if __name__ == "__main__":

    predictor = WorkloadPredictor()

    predicted_cpu = predictor.predict(
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

    print()
    print("=" * 50)
    print("WORKLOAD PREDICTION")
    print("=" * 50)
    print(f"Current CPU       : 60%")
    print(f"Request Rate      : 200 req/s")
    print(f"Predicted CPU     : {predicted_cpu}%")
    print(f"Prediction Horizon: +5 minutes")
    print("=" * 50)
