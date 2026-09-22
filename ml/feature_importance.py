import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

print("========================================")
print(" MEMBER 2 - FEATURE IMPORTANCE")
print("========================================")

DATA_FILE = "ml/data/ml_ready_dataset.csv"
MODEL_FILE = "ml/models/best_model.pkl"

# Load dataset
df = pd.read_csv(DATA_FILE)

# Same features used during training
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

# Load trained Random Forest
model = joblib.load(MODEL_FILE)

# Get feature importance
importance = model.feature_importances_

# Create dataframe
importance_df = pd.DataFrame({
    "feature": features,
    "importance": importance
})

# Sort from highest to lowest
importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance_df.to_string(index=False))

# Save CSV
importance_df.to_csv(
    "ml/plots/feature_importance.csv",
    index=False
)

# Create plot
os.makedirs("ml/plots", exist_ok=True)

plt.figure(figsize=(10, 7))

plt.barh(
    importance_df["feature"],
    importance_df["importance"]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Random Forest Feature Importance")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "ml/plots/feature_importance.png",
    dpi=150
)

plt.show()

print("\nFiles saved:")
print("ml/plots/feature_importance.csv")
print("ml/plots/feature_importance.png")

print("\n========================================")
print(" FEATURE IMPORTANCE COMPLETED")
print("========================================")