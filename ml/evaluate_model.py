import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

print("========================================")
print(" MEMBER 2 - MODEL EVALUATION")
print("========================================")

DATA_FILE = "ml/data/ml_ready_dataset.csv"
MODEL_FILE = "ml/models/best_model.pkl"

# Load data
df = pd.read_csv(DATA_FILE)

# Features
features = [
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

target = "target_cpu_5min"

# Same time-based split
split_index = int(len(df) * 0.8)

test_df = df.iloc[split_index:]

X_test = test_df[features]
y_test = test_df[target]

# Load model
model = joblib.load(MODEL_FILE)

# Predictions
predictions = model.predict(X_test)

# Create results dataframe
results = pd.DataFrame({
    "timestamp": test_df["timestamp"],
    "actual_cpu": y_test.values,
    "predicted_cpu": predictions
})

print("\nFirst 20 predictions:")
print(results.head(20).to_string(index=False))

print("\nPrediction statistics:")
print(results[["actual_cpu", "predicted_cpu"]].describe())

# Save predictions
os.makedirs("ml/plots", exist_ok=True)

results.to_csv(
    "ml/plots/predictions.csv",
    index=False
)

# Plot
plt.figure(figsize=(12, 6))

plt.plot(
    results["actual_cpu"].values,
    label="Actual CPU"
)

plt.plot(
    results["predicted_cpu"].values,
    label="Predicted CPU"
)

plt.xlabel("Test sample")
plt.ylabel("CPU (%)")
plt.title("Actual vs Predicted CPU - 5 Minute Forecast")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "ml/plots/actual_vs_predicted.png",
    dpi=150
)

plt.show()

print("\nGraph saved:")
print("ml/plots/actual_vs_predicted.png")

print("\n========================================")
print(" EVALUATION COMPLETED")
print("========================================")