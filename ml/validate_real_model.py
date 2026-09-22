import joblib
import pandas as pd
from pathlib import Path


DATA_FILE = Path(
    "ml/data/real_workload_dataset_v2.csv"
)

MODEL_FILE = Path(
    "ml/models/best_model.pkl"
)

FEATURE_FILE = Path(
    "ml/models/features.txt"
)


print("Loading real workload dataset...")

df = pd.read_csv(DATA_FILE)


print("Loading trained ML model...")

model = joblib.load(MODEL_FILE)


print("Loading model features...")

with open(FEATURE_FILE, "r") as file:
    features = [
        line.strip()
        for line in file
        if line.strip()
    ]


# --------------------------------------------------
# REAL DATA → MODEL FEATURES
# --------------------------------------------------

df["cpu_lag_1"] = (
    df["cpu_percent"]
    .shift(1)
)

df["cpu_lag_2"] = (
    df["cpu_percent"]
    .shift(2)
)

df["cpu_lag_3"] = (
    df["cpu_percent"]
    .shift(3)
)


df["request_lag_1"] = (
    df["request_rate"]
    .shift(1)
)

df["request_lag_2"] = (
    df["request_rate"]
    .shift(2)
)

df["request_lag_3"] = (
    df["request_rate"]
    .shift(3)
)


df["cpu_rolling_mean_3"] = (
    df["cpu_percent"]
    .rolling(3)
    .mean()
)


df["request_rolling_mean_3"] = (
    df["request_rate"]
    .rolling(3)
    .mean()
)


df["cpu_change"] = (
    df["cpu_percent"]
    .diff()
)


df["request_change"] = (
    df["request_rate"]
    .diff()
)


# --------------------------------------------------
# RENAME REAL DATA COLUMNS
# --------------------------------------------------

df = df.rename(
    columns={
        "cpu_percent": "cpu",
        "memory_used_mib": "memory",
        "network_rx_rate_mib_s": "network",
        "latency_ms": "latency"
    }
)


# --------------------------------------------------
# REMOVE INITIAL NaN ROWS
# --------------------------------------------------

df = df.dropna(
    subset=features
).copy()


# --------------------------------------------------
# PREDICT
# --------------------------------------------------

X = df[features]

df["predicted_cpu_5min"] = (
    model.predict(X)
)


# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

print()
print("=" * 70)
print("REAL DATA MODEL VALIDATION")
print("=" * 70)

print()

print(
    df[
        [
            "timestamp",
            "cpu",
            "request_rate",
            "latency",
            "predicted_cpu_5min"
        ]
    ].to_string(
        index=False
    )
)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

print(
    f"Observations tested : {len(df)}"
)

print(
    f"Actual CPU range    : "
    f"{df['cpu'].min():.2f}% - "
    f"{df['cpu'].max():.2f}%"
)

print(
    f"Predicted CPU range : "
    f"{df['predicted_cpu_5min'].min():.2f}% - "
    f"{df['predicted_cpu_5min'].max():.2f}%"
)

print(
    f"Average actual CPU  : "
    f"{df['cpu'].mean():.2f}%"
)

print(
    f"Average prediction  : "
    f"{df['predicted_cpu_5min'].mean():.2f}%"
)