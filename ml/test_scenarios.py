import pandas as pd
import joblib

MODEL_FILE = "ml/models/best_model.pkl"

model = joblib.load(MODEL_FILE)

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


def predict(data):
    df = pd.DataFrame([data])
    return float(model.predict(df[FEATURES])[0])


# ==================================================
# SCENARIO 1 - NORMAL WORKLOAD
# ==================================================

normal = {
    "cpu": 40,
    "memory": 48,
    "request_rate": 100,
    "network": 8,
    "latency": 22,
    "resource_count": 2,

    "cpu_lag_1": 39,
    "cpu_lag_2": 40,
    "cpu_lag_3": 38,

    "request_lag_1": 98,
    "request_lag_2": 95,
    "request_lag_3": 97,

    "cpu_rolling_mean_3": 39,
    "request_rolling_mean_3": 98,

    "cpu_change": 1,
    "request_change": 2
}


# ==================================================
# SCENARIO 2 - INCREASING WORKLOAD
# ==================================================

increasing = {
    "cpu": 68,
    "memory": 58,
    "request_rate": 250,
    "network": 22,
    "latency": 29,
    "resource_count": 2,

    "cpu_lag_1": 63,
    "cpu_lag_2": 59,
    "cpu_lag_3": 55,

    "request_lag_1": 225,
    "request_lag_2": 200,
    "request_lag_3": 175,

    "cpu_rolling_mean_3": 63.33,
    "request_rolling_mean_3": 225,

    "cpu_change": 5,
    "request_change": 25
}


# ==================================================
# SCENARIO 3 - SUDDEN SPIKE
# ==================================================

spike = {
    "cpu": 82,
    "memory": 65,
    "request_rate": 400,
    "network": 35,
    "latency": 38,
    "resource_count": 2,

    "cpu_lag_1": 65,
    "cpu_lag_2": 58,
    "cpu_lag_3": 52,

    "request_lag_1": 220,
    "request_lag_2": 180,
    "request_lag_3": 150,

    "cpu_rolling_mean_3": 68.33,
    "request_rolling_mean_3": 270,

    "cpu_change": 17,
    "request_change": 180
}


# ==================================================
# RUN TESTS
# ==================================================

scenarios = {
    "NORMAL WORKLOAD": normal,
    "INCREASING WORKLOAD": increasing,
    "SUDDEN SPIKE": spike
}

print("========================================")
print(" MEMBER 2 - WORKLOAD SCENARIO TEST")
print("========================================")

for name, data in scenarios.items():

    prediction = predict(data)

    print("\n----------------------------------------")
    print(name)
    print("----------------------------------------")

    print(f"Current CPU       : {data['cpu']}%")
    print(f"Request Rate      : {data['request_rate']} req/min")
    print(f"Current Resources : {data['resource_count']}")
    print(f"Predicted CPU +5m : {prediction:.2f}%")

    if prediction >= 80:
        print("Prediction Status : HIGH CPU")
        print("Suggested Action  : SCALE_UP")

    elif prediction < 30:
        print("Prediction Status : LOW CPU")
        print("Suggested Action  : POSSIBLE SCALE_DOWN")

    else:
        print("Prediction Status : NORMAL")
        print("Suggested Action  : NO_ACTION")


print("\n========================================")
print(" SCENARIO TEST COMPLETED")
print("========================================")