import psycopg2
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "cloud_orchestrator",
    "user": "postgres",
    "password": "postgres"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cpu FLOAT,
            memory FLOAT,
            request_rate FLOAT,
            network FLOAT,
            latency FLOAT,
            resource_count INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metric_id INTEGER,
            current_cpu FLOAT,
            predicted_cpu FLOAT,
            FOREIGN KEY (metric_id) REFERENCES metrics(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            prediction_id INTEGER,
            decision VARCHAR(50),
            reason TEXT,
            weighted_score FLOAT,
            FOREIGN KEY (prediction_id) REFERENCES predictions(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS action_history (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            decision_id INTEGER,
            action VARCHAR(50),
            status VARCHAR(50),
            details TEXT,
            FOREIGN KEY (decision_id) REFERENCES decisions(id)
        );
    """)

    connection.commit()

    cursor.close()
    connection.close()

    print("========================================")
    print("DATABASE INITIALIZED")
    print("========================================")
    print("✓ metrics")
    print("✓ predictions")
    print("✓ decisions")
    print("✓ action_history")
    print("========================================")


if __name__ == "__main__":
    create_tables()