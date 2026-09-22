import pandas as pd

INPUT_FILE = "ml/data/workload_dataset.csv"
OUTPUT_FILE = "ml/data/ml_ready_dataset.csv"

print("========================================")
print(" MEMBER 2 - FEATURE ENGINEERING")
print("========================================")

# Load dataset
df = pd.read_csv(INPUT_FILE)

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort chronologically
df = df.sort_values("timestamp").reset_index(drop=True)

print("\nOriginal dataset:")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

# Previous CPU values
df["cpu_lag_1"] = df["cpu"].shift(1)
df["cpu_lag_2"] = df["cpu"].shift(2)
df["cpu_lag_3"] = df["cpu"].shift(3)

# Previous request rates
df["request_lag_1"] = df["request_rate"].shift(1)
df["request_lag_2"] = df["request_rate"].shift(2)
df["request_lag_3"] = df["request_rate"].shift(3)

# Rolling averages
df["cpu_rolling_mean_3"] = df["cpu"].rolling(window=3).mean()
df["request_rolling_mean_3"] = df["request_rate"].rolling(window=3).mean()

# Trends
df["cpu_change"] = df["cpu"] - df["cpu_lag_1"]
df["request_change"] = df["request_rate"] - df["request_lag_1"]

# Target: CPU 5 minutes into the future
df["target_cpu_5min"] = df["cpu"].shift(-5)

# Remove rows with missing values
df = df.dropna().reset_index(drop=True)

# Save ML-ready dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nFeature engineering completed.")

print("\nFinal columns:")
print(list(df.columns))

print("\nFinal dataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nTarget statistics:")
print(df["target_cpu_5min"].describe())

print("\nSaved:")
print(OUTPUT_FILE)

print("========================================")