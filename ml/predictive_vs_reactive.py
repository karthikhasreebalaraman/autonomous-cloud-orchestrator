import pandas as pd


print()
print("=" * 70)
print("PREDICTIVE VS REACTIVE AUTOSCALING")
print("=" * 70)


# ---------------------------------------------------------
# DEMO WORKLOAD
# ---------------------------------------------------------

data = pd.DataFrame({
    "time": [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5"
    ],

    "current_cpu": [
        55,
        62,
        70,
        78,
        88
    ],

    "predicted_cpu": [
        62,
        70,
        78,
        88,
        94
    ]
})


# ---------------------------------------------------------
# REACTIVE DECISION
# ---------------------------------------------------------

data["reactive_action"] = data["current_cpu"].apply(
    lambda cpu:
        "SCALE_UP"
        if cpu > 80
        else "NO_ACTION"
)


# ---------------------------------------------------------
# PREDICTIVE DECISION
# ---------------------------------------------------------

data["predictive_action"] = data["predicted_cpu"].apply(
    lambda cpu:
        "SCALE_UP"
        if cpu > 80
        else "NO_ACTION"
)


print("\nWORKLOAD COMPARISON")
print("-" * 70)

print(
    data.to_string(index=False)
)


print("\n")
print("=" * 70)
print("OBSERVATION")
print("=" * 70)

print(
    "\nReactive scaling waits until current CPU crosses 80%."
)

print(
    "Predictive scaling can trigger when future CPU is "
    "predicted to cross 80%."
)

print(
    "\nThis demonstrates the architectural difference between "
    "reactive and predictive autoscaling."
)


print("\n" + "=" * 70)