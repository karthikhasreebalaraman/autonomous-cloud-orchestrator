import pandas as pd
import numpy as np

print("========================================")
print(" MEMBER 2 - REALISTIC WORKLOAD DATASET")
print("========================================")

np.random.seed(42)

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

samples = 1440
timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    periods=samples,
    freq="min"
)

# --------------------------------------------------
# WORKLOAD GENERATION
# --------------------------------------------------

request_rate = np.zeros(samples)

# Starting workload
request_rate[0] = 40

for i in range(1, samples):

    hour = timestamps[i].hour

    # Daily baseline
    if 0 <= hour < 6:
        baseline = 45
    elif 6 <= hour < 10:
        baseline = 100
    elif 10 <= hour < 17:
        baseline = 180
    elif 17 <= hour < 22:
        baseline = 120
    else:
        baseline = 60

    # Slowly move toward baseline
    change = (baseline - request_rate[i - 1]) * 0.08

    # Small natural workload variation
    noise = np.random.normal(0, 5)

    request_rate[i] = (
        request_rate[i - 1]
        + change
        + noise
    )

# --------------------------------------------------
# SUSTAINED WORKLOAD SPIKES
# --------------------------------------------------

spikes = [
    (420, 450, 300),
    (720, 760, 400),
    (1000, 1035, 350),
    (1180, 1210, 280)
]

for start, end, spike_value in spikes:

    for i in range(start, end):

        # Smooth spike instead of instant random jump
        progress = (i - start) / (end - start)

        if progress < 0.5:
            factor = progress * 2
        else:
            factor = (1 - progress) * 2

        request_rate[i] += spike_value * factor

request_rate = np.clip(
    request_rate,
    20,
    500
)

# --------------------------------------------------
# CPU GENERATION
# --------------------------------------------------

cpu = np.zeros(samples)

for i in range(samples):

    # CPU depends on current workload
    workload_component = request_rate[i] * 0.20

    # CPU also has inertia from previous minute
    if i == 0:
        previous_cpu = 30
    else:
        previous_cpu = cpu[i - 1]

    target_cpu = 20 + workload_component

    cpu[i] = (
        0.65 * previous_cpu
        + 0.35 * target_cpu
        + np.random.normal(0, 1.5)
    )

cpu = np.clip(cpu, 5, 98)

# --------------------------------------------------
# MEMORY
# --------------------------------------------------

memory = (
    35
    + cpu * 0.35
    + np.random.normal(0, 2, samples)
)

memory = np.clip(memory, 20, 95)

# --------------------------------------------------
# NETWORK
# --------------------------------------------------

network = (
    request_rate * 0.085
    + np.random.normal(0, 1.5, samples)
)

network = np.clip(network, 1, 50)

# --------------------------------------------------
# LATENCY
# --------------------------------------------------

latency = (
    15
    + cpu * 0.18
    + np.maximum(cpu - 70, 0) * 0.35
    + np.random.normal(0, 1.5, samples)
)

latency = np.clip(latency, 10, 100)

# --------------------------------------------------
# RESOURCE COUNT
# --------------------------------------------------

resource_count = np.where(
    cpu >= 80,
    3,
    2
)

# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame({
    "timestamp": timestamps,
    "cpu": np.round(cpu, 2),
    "memory": np.round(memory, 2),
    "request_rate": np.round(request_rate, 2),
    "network": np.round(network, 2),
    "latency": np.round(latency, 2),
    "resource_count": resource_count
})

# --------------------------------------------------
# SAVE
# --------------------------------------------------

output_file = "ml/data/workload_dataset.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nDataset generated successfully.")

print(f"Samples: {len(df)}")
print(f"Output : {output_file}")

print("\nColumns:")
print(list(df.columns))

print("\nFirst 10 rows:")
print(df.head(10).to_string(index=False))

print("\nDataset statistics:")
print(df.describe().to_string())

print("\n========================================")
print(" DATASET GENERATION COMPLETED")
print("========================================")