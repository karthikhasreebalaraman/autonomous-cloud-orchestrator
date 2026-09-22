import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = Path("ml/data/real_workload_metrics_v3.csv")
REQUEST_FILE = Path("ml/data/request_metrics_v3.csv")
OUTPUT_FILE = Path("ml/data/real_workload_dataset_v4.csv")

print("=" * 70)
print("REAL WORKLOAD DATASET PREPARATION V4")
print("=" * 70)

# ---------------------------------------------------------
# 1. LOAD DOCKER METRICS
# ---------------------------------------------------------

print("\nLoading Docker metrics...")

metrics = pd.read_csv(INPUT_FILE)

metrics["timestamp"] = pd.to_datetime(metrics["timestamp"])

metrics = metrics.sort_values("timestamp")

# We train using the main container only.
metrics = metrics[
    metrics["container_name"] == "cloud-app"
].copy()

print(f"Docker rows: {len(metrics)}")

# ---------------------------------------------------------
# 2. CONVERT MEMORY
# ---------------------------------------------------------

metrics["memory_used_mib"] = pd.to_numeric(
    metrics["memory_used_mib"],
    errors="coerce"
)

# ---------------------------------------------------------
# 3. CONVERT NETWORK VALUES
# ---------------------------------------------------------

def parse_network(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    try:
        if value.endswith("kB"):
            return float(value.replace("kB", "").strip()) / 1024

        if value.endswith("MB"):
            return float(value.replace("MB", "").strip())

        if value.endswith("MiB"):
            return float(value.replace("MiB", "").strip())

        if value.endswith("GB"):
            return float(value.replace("GB", "").strip()) * 1024

        if value.endswith("GiB"):
            return float(value.replace("GiB", "").strip()) * 1024

        if value.endswith("B"):
            return float(value.replace("B", "").strip()) / (1024 * 1024)

        return float(value)

    except:
        return np.nan


metrics["network_rx_mib"] = metrics["network_rx"].apply(parse_network)
metrics["network_tx_mib"] = metrics["network_tx"].apply(parse_network)

# ---------------------------------------------------------
# 4. REMOVE DUPLICATES
# ---------------------------------------------------------

metrics = metrics.drop_duplicates(
    subset=["timestamp"],
    keep="last"
)

metrics = metrics.set_index("timestamp")

# ---------------------------------------------------------
# 5. CREATE COMPLETE 5-SECOND TIMELINE
# ---------------------------------------------------------

print("Creating continuous 5-second timeline...")

full_index = pd.date_range(
    start=metrics.index.min(),
    end=metrics.index.max(),
    freq="5s"
)

metrics = metrics.reindex(full_index)

metrics.index.name = "timestamp"

# ---------------------------------------------------------
# 6. FILL CPU / MEMORY / RESOURCE COUNT
# ---------------------------------------------------------

metrics["cpu_percent"] = (
    metrics["cpu_percent"]
    .interpolate()
    .ffill()
    .bfill()
)

metrics["memory_used_mib"] = (
    metrics["memory_used_mib"]
    .interpolate()
    .ffill()
    .bfill()
)

metrics["resource_count"] = (
    metrics["resource_count"]
    .ffill()
    .bfill()
)

# ---------------------------------------------------------
# 7. NETWORK RATE
# ---------------------------------------------------------

metrics["network_rx_rate_mib_s"] = (
    metrics["network_rx_mib"]
    .diff()
    .clip(lower=0)
    / 5
)

metrics["network_tx_rate_mib_s"] = (
    metrics["network_tx_mib"]
    .diff()
    .clip(lower=0)
    / 5
)

# Missing / unchanged network values mean approximately
# zero observed traffic during that interval.

metrics["network_rx_rate_mib_s"] = (
    metrics["network_rx_rate_mib_s"]
    .fillna(0)
)

metrics["network_tx_rate_mib_s"] = (
    metrics["network_tx_rate_mib_s"]
    .fillna(0)
)

# ---------------------------------------------------------
# 8. LOAD REQUEST DATA
# ---------------------------------------------------------

print("Loading request metrics...")

requests = pd.read_csv(REQUEST_FILE)

requests["timestamp"] = pd.to_datetime(
    requests["timestamp"]
)

requests = requests.sort_values("timestamp")

# Create 5-second request windows
requests = requests.set_index("timestamp")

request_count = (
    requests["request_number"]
    .resample("5s")
    .count()
)

request_rate = request_count / 5

latency = (
    requests["latency_ms"]
    .resample("5s")
    .mean()
)

request_data = pd.DataFrame({
    "request_rate": request_rate,
    "latency_ms": latency
})

# ---------------------------------------------------------
# 9. ALIGN REQUEST DATA WITH DOCKER TIMELINE
# ---------------------------------------------------------

dataset = metrics[
    [
        "cpu_percent",
        "memory_used_mib",
        "network_rx_rate_mib_s",
        "network_tx_rate_mib_s",
        "resource_count"
    ]
].copy()

dataset = dataset.join(
    request_data,
    how="left"
)

# No requests = zero request rate.
dataset["request_rate"] = (
    dataset["request_rate"]
    .fillna(0)
)

# No request = no measured request latency.
dataset["latency_ms"] = (
    dataset["latency_ms"]
    .fillna(0)
)

# ---------------------------------------------------------
# 10. CLEAN DATA
# ---------------------------------------------------------

dataset = dataset.replace(
    [np.inf, -np.inf],
    np.nan
)

dataset = dataset.dropna()

# ---------------------------------------------------------
# 11. RESET INDEX
# ---------------------------------------------------------

dataset = dataset.reset_index()

# ---------------------------------------------------------
# 12. SAVE
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

dataset.to_csv(
    OUTPUT_FILE,
    index=False
)

# ---------------------------------------------------------
# 13. PRINT RESULTS
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("DATASET CREATED")
print("=" * 70)

print(f"Rows    : {len(dataset)}")
print(f"Columns : {len(dataset.columns)}")
print(f"Saved   : {OUTPUT_FILE}")

print("\nColumns:")
for column in dataset.columns:
    print(" -", column)

print("\nStatistics:")
print(
    dataset[
        [
            "cpu_percent",
            "memory_used_mib",
            "network_rx_rate_mib_s",
            "network_tx_rate_mib_s",
            "request_rate",
            "latency_ms",
            "resource_count"
        ]
    ].describe()
)

print("\nCPU range:")
print(
    f"Min : {dataset['cpu_percent'].min():.2f}%"
)
print(
    f"Max : {dataset['cpu_percent'].max():.2f}%"
)

print("\nRequest rate range:")
print(
    f"Min : {dataset['request_rate'].min():.2f} req/s"
)
print(
    f"Max : {dataset['request_rate'].max():.2f} req/s"
)

print("\nDataset preparation complete.")