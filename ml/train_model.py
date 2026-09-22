import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor

import joblib
import os

print("========================================")
print(" MEMBER 2 - MODEL TRAINING")
print("========================================")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

DATA_FILE = "ml/data/ml_ready_dataset.csv"

df = pd.read_csv(DATA_FILE)

print(f"\nDataset loaded: {df.shape}")

# --------------------------------------------------
# FEATURES AND TARGET
# --------------------------------------------------

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

X = df[features]
y = df[target]

# --------------------------------------------------
# TIME-BASED TRAIN / TEST SPLIT
# --------------------------------------------------

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTime-based split:")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")

# --------------------------------------------------
# MODELS
# --------------------------------------------------

models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    ),

    "XGBoost": XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42
    )
}

results = {}

# --------------------------------------------------
# TRAIN AND EVALUATE
# --------------------------------------------------

for name, model in models.items():

    print("\n----------------------------------------")
    print(f"Training: {name}")
    print("----------------------------------------")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(y_test, predictions)

    results[name] = {
        "model": model,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R²   : {r2:.4f}")

# --------------------------------------------------
# MODEL COMPARISON
# --------------------------------------------------

print("\n========================================")
print(" MODEL COMPARISON")
print("========================================")

for name, result in results.items():

    print(
        f"{name:<20} "
        f"MAE={result['MAE']:.4f}   "
        f"RMSE={result['RMSE']:.4f}   "
        f"R²={result['R2']:.4f}"
    )

# --------------------------------------------------
# SELECT BEST MODEL
# --------------------------------------------------

best_name = min(
    results,
    key=lambda name: results[name]["RMSE"]
)

best_model = results[best_name]["model"]

print("\n========================================")
print(" BEST MODEL")
print("========================================")

print(f"Selected model: {best_name}")
print(f"RMSE: {results[best_name]['RMSE']:.4f}")
print(f"MAE : {results[best_name]['MAE']:.4f}")
print(f"R²  : {results[best_name]['R2']:.4f}")

# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

os.makedirs("ml/models", exist_ok=True)

model_path = "ml/models/best_model.pkl"

joblib.dump(best_model, model_path)

print(f"\nModel saved to:")
print(model_path)

# Save feature list
features_path = "ml/models/features.txt"

with open(features_path, "w") as f:
    for feature in features:
        f.write(feature + "\n")

print(f"Features saved to:")
print(features_path)

print("\n========================================")
print(" TRAINING COMPLETED")
print("========================================")