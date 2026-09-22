from decision_engine.prediction_client import get_prediction
from decision_engine.decision_model import calculate_decision
from decision_engine.executor import execute_decision


print()
print("=" * 70)
print("AUTONOMOUS PREDICTIVE SCALE-UP TEST")
print("=" * 70)


# =================================================
# 1. SIMULATED SHARP WORKLOAD INCREASE
# =================================================

current_cpu = 82
memory = 70
request_rate = 400
network = 35
latency = 55
resource_count = 3

cpu_lag_1 = 78
cpu_lag_2 = 72
cpu_lag_3 = 65

request_lag_1 = 350
request_lag_2 = 300
request_lag_3 = 250

cpu_rolling_mean_3 = 77
request_rolling_mean_3 = 350

cpu_change = 4
request_change = 50


# =================================================
# 2. MEMBER 2 — ML PREDICTION
# =================================================

prediction = get_prediction(

    current_cpu=current_cpu,
    memory=memory,
    request_rate=request_rate,
    network=network,
    latency=latency,
    resource_count=resource_count,

    cpu_lag_1=cpu_lag_1,
    cpu_lag_2=cpu_lag_2,
    cpu_lag_3=cpu_lag_3,

    request_lag_1=request_lag_1,
    request_lag_2=request_lag_2,
    request_lag_3=request_lag_3,

    cpu_rolling_mean_3=cpu_rolling_mean_3,
    request_rolling_mean_3=request_rolling_mean_3,

    cpu_change=cpu_change,
    request_change=request_change
)

predicted_cpu = prediction["predicted_cpu"]


# =================================================
# 3. DISPLAY WORKLOAD
# =================================================

print("\nCURRENT WORKLOAD")
print("----------------")
print(f"CPU          : {current_cpu}%")
print(f"Memory       : {memory}%")
print(f"Request Rate : {request_rate} req/s")
print(f"Latency      : {latency} ms")
print(f"Containers   : {resource_count}")


# =================================================
# 4. DISPLAY PREDICTION
# =================================================

print("\nML PREDICTION")
print("-------------")
print(f"Predicted CPU (+5 min): {predicted_cpu}%")


# =================================================
# 5. MEMBER 3 — DECISION INTELLIGENCE
# =================================================

decision_result = calculate_decision(

    current_cpu=current_cpu,

    predicted_cpu=predicted_cpu,

    memory=memory,

    running_containers=resource_count,

    healthy=True
)


decision = decision_result["decision"]


print("\nDECISION INTELLIGENCE")
print("---------------------")
print(f"Decision : {decision}")
print(f"Reason   : {decision_result['reason']}")
print(f"Score    : {decision_result['weighted_score']}")


# =================================================
# 6. AUTOMATIC EXECUTION
# =================================================

print("\nAUTOMATIC EXECUTION")
print("-------------------")

execution_result = execute_decision(
    decision
)


# =================================================
# 7. FINAL RESULT
# =================================================

print("\nFINAL RESULT")
print("------------")
print(f"Decision : {decision}")
print(
    f"Execution Status : "
    f"{execution_result.get('status')}"
)

if execution_result.get("container"):
    print(
        f"New Container : "
        f"{execution_result.get('container')}"
    )

print("\n" + "=" * 70)