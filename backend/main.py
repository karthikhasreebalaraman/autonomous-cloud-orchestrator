from fastapi import FastAPI
from datetime import datetime

from decision_engine.infrastructure_client import (
    get_status,
    scale_up,
    scale_down,
    recover,
    restart,
    replace,
    redistribute
)

from decision_engine.prediction_client import get_prediction
from decision_engine.decision_model import calculate_decision

from decision_engine.protection import (
    can_scale_up,
    can_scale_down,
    record_action
)

from Database.db import get_connection


app = FastAPI(
    title="Autonomous Cloud Infrastructure Orchestrator",
    description="Decision Intelligence Backend",
    version="1.0.0"
)


def get_workload_data():

    current_cpu = 85
    memory = 75
    request_rate = 500
    network = 30
    latency = 45

    infrastructure = get_status()
    resource_count = infrastructure["running"]

    prediction = get_prediction(
        current_cpu=current_cpu,
        memory=memory,
        request_rate=request_rate,
        network=network,
        latency=latency,
        resource_count=resource_count,
        cpu_lag_1=80,
        cpu_lag_2=75,
        cpu_lag_3=70,
        request_lag_1=450,
        request_lag_2=400,
        request_lag_3=350,
        cpu_rolling_mean_3=75,
        request_rolling_mean_3=400,
        cpu_change=5,
        request_change=50
    )

    return {
        "current_cpu": current_cpu,
        "memory": memory,
        "request_rate": request_rate,
        "network": network,
        "latency": latency,
        "resource_count": resource_count,
        "prediction": prediction
    }


def execute_action(decision, running_containers):

    if decision == "SCALE_UP":

        allowed, message = can_scale_up(running_containers)

        if not allowed:
            return {
                "action": "SCALE_UP",
                "status": "BLOCKED",
                "message": message
            }

        result = scale_up()

        if result.get("status") == "SUCCESS":
            record_action()

        return result

    if decision == "SCALE_DOWN":

        allowed, message = can_scale_down(running_containers)

        if not allowed:
            return {
                "action": "SCALE_DOWN",
                "status": "BLOCKED",
                "message": message
            }

        result = scale_down()

        if result.get("status") == "SUCCESS":
            record_action()

        return result

    if decision == "RECOVER":

        result = recover()

        if result.get("status") == "SUCCESS":
            record_action()

        return result

    if decision == "RESTART":

        result = restart()

        if result.get("status") == "SUCCESS":
            record_action()

        return result

    if decision == "REPLACE":

        result = replace()

        if result.get("status") == "SUCCESS":
            record_action()

        return result

    if decision == "REDISTRIBUTE":

        result = redistribute()

        if result.get("status") == "SUCCESS":
            record_action()

        return result

    return {
        "action": "NO_ACTION",
        "status": "NO_EXECUTION"
    }


def save_execution_to_database(
    data,
    prediction,
    decision_result,
    execution_result
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO metrics
        (cpu, memory, request_rate, network, latency, resource_count)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        data["current_cpu"],
        data["memory"],
        data["request_rate"],
        data["network"],
        data["latency"],
        data["resource_count"]
    ))

    metric_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO predictions
        (metric_id, current_cpu, predicted_cpu)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (
        metric_id,
        prediction["current_cpu"],
        prediction["predicted_cpu"]
    ))

    prediction_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO decisions
        (prediction_id, decision, reason, weighted_score)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (
        prediction_id,
        decision_result["decision"],
        decision_result["reason"],
        decision_result["weighted_score"]
    ))

    decision_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO action_history
        (decision_id, action, status, details)
        VALUES (%s, %s, %s, %s)
    """, (
        decision_id,
        execution_result.get(
            "action",
            decision_result["decision"]
        ),
        execution_result.get(
            "status",
            "UNKNOWN"
        ),
        str(execution_result)
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "metric_id": metric_id,
        "prediction_id": prediction_id,
        "decision_id": decision_id
    }


@app.get("/")
def root():

    return {
        "system": "Autonomous Cloud Infrastructure Orchestrator",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/infrastructure")
def infrastructure_status():

    return get_status()


@app.get("/predict")
def predict():

    data = get_workload_data()

    prediction = data["prediction"]

    return {
        "current_cpu": prediction["current_cpu"],
        "memory": prediction["memory"],
        "request_rate": prediction["request_rate"],
        "predicted_cpu": prediction["predicted_cpu"],
        "running_containers": data["resource_count"]
    }


@app.get("/decision")
def decision():

    data = get_workload_data()

    prediction = data["prediction"]

    result = calculate_decision(
        current_cpu=data["current_cpu"],
        predicted_cpu=prediction["predicted_cpu"],
        memory=data["memory"],
        running_containers=data["resource_count"],
        healthy=True
    )

    return {
        "current_cpu": data["current_cpu"],
        "predicted_cpu": prediction["predicted_cpu"],
        "running_containers": data["resource_count"],
        "decision": result["decision"],
        "reason": result["reason"],
        "weighted_score": result["weighted_score"],
        "scores": result["scores"]
    }


@app.post("/execute")
def execute():

    data = get_workload_data()

    prediction = data["prediction"]

    result = calculate_decision(
        current_cpu=data["current_cpu"],
        predicted_cpu=prediction["predicted_cpu"],
        memory=data["memory"],
        running_containers=data["resource_count"],
        healthy=True
    )

    decision_name = result["decision"]

    execution_result = execute_action(
        decision_name,
        data["resource_count"]
    )

    database_ids = save_execution_to_database(
        data,
        prediction,
        result,
        execution_result
    )

    final_infrastructure = get_status()

    return {
        "timestamp": datetime.now().isoformat(),

        "workload": {
            "current_cpu": data["current_cpu"],
            "memory": data["memory"],
            "request_rate": data["request_rate"],
            "network": data["network"],
            "latency": data["latency"]
        },

        "prediction": {
            "predicted_cpu": prediction["predicted_cpu"]
        },

        "decision": {
            "action": decision_name,
            "reason": result["reason"],
            "weighted_score": result["weighted_score"],
            "scores": result["scores"]
        },

        "execution": execution_result,

        "database": database_ids,

        "final_infrastructure": final_infrastructure
    }