import joblib
import pandas as pd

from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


DATA_FILE = Path("ml/data/real_workload_dataset_v3.csv")
MODEL_FILE = Path("ml/models/best_real_model.pkl")
FEATURE_FILE = Path("ml/models/real_features.txt")
RESULT_FILE = Path("ml/plots/real_model_comparison.csv")


print("=" * 70)
print("REAL DOCKER MODEL TRAINING V2")
print("=" * 70)

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------

print("\nLoading real workload dataset...")

df = pd.read_csv(DATA_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values("timestamp").reset_index(drop=True)

print(f"Raw rows: {len(df)}")


# ---------------------------------------------------------
# 2. CLEAN NUMERIC VALUES
# ---------------------------------------------------------

numeric_columns = [
    "cpu_percent",
    "memory_used_mib",
    "network_rx_rate_mib_s",
    "network_tx_rate_mib_s",
    "resource_count",
    "request_rate",
    "latency_ms"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Missing network measurements = zero observed rate
df["network_rx_rate_mib_s"] = (
    df["network_rx_rate_mib_s"]
    .fillna(0)
)

df["network_tx_rate_mib_s"] = (
    df["network_tx_rate_mib_s"]
    .fillna(0)
)

df = df.dropna(
    subset=[
        "cpu_percent",
        "memory_used_mib",
        "resource_count",
        "request_rate",
        "latency_ms"
    ]
).reset_index(drop=True)


# ---------------------------------------------------------
# 3. FEATURE ENGINEERING
# ---------------------------------------------------------

print("\nCreating features...")

df["cpu_lag_1"] = df["cpu_percent"].shift(1)
df["cpu_lag_2"] = df["cpu_percent"].shift(2)
df["cpu_lag_3"] = df["cpu_percent"].shift(3)

df["request_lag_1"] = df["request_rate"].shift(1)
df["request_lag_2"] = df["request_rate"].shift(2)
df["request_lag_3"] = df["request_rate"].shift(3)

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
    df["cpu_percent"].diff()
)

df["request_change"] = (
    df["request_rate"].diff()
)


# ---------------------------------------------------------
# 4. CREATE TRUE APPROXIMATE 5-MIN TARGET
# ---------------------------------------------------------

print("Creating 5-minute future CPU target...")

future = df[
    ["timestamp", "cpu_percent"]
].copy()

future = future.rename(
    columns={
        "timestamp": "future_timestamp",
        "cpu_percent": "target_cpu_5min"
    }
)

# Target timestamp = current timestamp + 5 minutes
df["target_timestamp"] = (
    df["timestamp"] +
    pd.Timedelta(minutes=5)
)

# Find nearest future observation to +5 minutes
df = pd.merge_asof(
    df.sort_values("target_timestamp"),
    future.sort_values("future_timestamp"),
    left_on="target_timestamp",
    right_on="future_timestamp",
    direction="nearest",
    tolerance=pd.Timedelta(seconds=15)
)

# Remove helper columns
df = df.drop(
    columns=[
        "target_timestamp",
        "future_timestamp"
    ]
)


# ---------------------------------------------------------
# 5. FEATURES
# ---------------------------------------------------------

features = [
    "cpu_percent",
    "memory_used_mib",
    "network_rx_rate_mib_s",
    "network_tx_rate_mib_s",
    "request_rate",
    "latency_ms",

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


# ---------------------------------------------------------
# 6. REMOVE INVALID ROWS
# ---------------------------------------------------------

df = df.dropna(
    subset=features + [target]
).reset_index(drop=True)

print(f"Usable rows: {len(df)}")


if len(df) < 20:
    raise ValueError(
        "Not enough usable rows for real-data training."
    )


# ---------------------------------------------------------
# 7. TIME-BASED TRAIN / TEST SPLIT
# ---------------------------------------------------------

split_index = int(
    len(df) * 0.8
)

train = df.iloc[:split_index]
test = df.iloc[split_index:]

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]

print(f"Training rows: {len(train)}")
print(f"Testing rows : {len(test)}")


# ---------------------------------------------------------
# 8. MODELS
# ---------------------------------------------------------

models = {

    "Linear Regression":
        LinearRegression(),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=300,
            max_depth=8,
            random_state=42,
            n_jobs=-1
        )
}


if XGBOOST_AVAILABLE:

    models["XGBoost"] = XGBRegressor(

        n_estimators=300,

        max_depth=4,

        learning_rate=0.05,

        subsample=0.8,

        colsample_bytree=0.8,

        objective="reg:squarederror",

        random_state=42
    )


# ---------------------------------------------------------
# 9. TRAIN + EVALUATE
# ---------------------------------------------------------

results = []

trained_models = {}

print()
print("=" * 70)
print("REAL DATA MODEL COMPARISON")
print("=" * 70)


for name, model in models.items():

    print()
    print(f"Training {name}...")

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    print(
        f"MAE  : {mae:.4f}"
    )

    print(
        f"RMSE : {rmse:.4f}"
    )

    print(
        f"R²   : {r2:.4f}"
    )

    results.append({

        "model": name,

        "MAE": mae,

        "RMSE": rmse,

        "R2": r2
    })

    trained_models[name] = model


# ---------------------------------------------------------
# 10. RESULTS
# ---------------------------------------------------------

results_df = pd.DataFrame(
    results
)

results_df = (
    results_df
    .sort_values("RMSE")
    .reset_index(drop=True)
)


print()
print("=" * 70)
print("MODEL RESULTS")
print("=" * 70)

print(
    results_df.to_string(
        index=False
    )
)


# ---------------------------------------------------------
# 11. SELECT BEST MODEL
# ---------------------------------------------------------

best_name = (
    results_df.iloc[0]["model"]
)

best_model = (
    trained_models[best_name]
)

print()
print(
    f"Best real-data model: {best_name}"
)


# ---------------------------------------------------------
# 12. SAVE MODEL
# ---------------------------------------------------------

MODEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    best_model,
    MODEL_FILE
)


# ---------------------------------------------------------
# 13. SAVE FEATURES
# ---------------------------------------------------------

with open(
    FEATURE_FILE,
    "w"
) as file:

    for feature in features:

        file.write(
            feature + "\n"
        )


# ---------------------------------------------------------
# 14. SAVE RESULTS
# ---------------------------------------------------------

RESULT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

results_df.to_csv(
    RESULT_FILE,
    index=False
)


# ---------------------------------------------------------
# 15. FINAL SUMMARY
# ---------------------------------------------------------

print()
print("=" * 70)
print("FILES SAVED")
print("=" * 70)

print(
    f"Model    : {MODEL_FILE}"
)

print(
    f"Features : {FEATURE_FILE}"
)

print(
    f"Results  : {RESULT_FILE}"
)

print()
print("Real-data training complete.")