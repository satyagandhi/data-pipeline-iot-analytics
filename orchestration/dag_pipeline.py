"""
Airflow DAG — IoT Analytics Pipeline
Orchestrates the full pipeline on a daily schedule.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "satya_gandhi",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
}


def ingest_task():
    from ingestion.stream_ingestor import ingest_events, normalise_schema
    df = ingest_events("data/sample_iot_events.json")
    df = normalise_schema(df)
    df.to_parquet("data/ingested.parquet", index=False)
    print(f"[DAG] Ingested {len(df)} records")


def validate_task():
    import pandas as pd
    from quality.schema_validator import validate_schema
    df = pd.read_parquet("data/ingested.parquet")
    report = validate_schema(df)
    print(f"[DAG] Validation complete: {report}")


def transform_task():
    import pandas as pd
    from quality.anomaly_detector import detect_anomalies
    from models.feature_engineering import engineer_features
    df = pd.read_parquet("data/ingested.parquet")
    df = detect_anomalies(df, columns=["temperature", "pressure"])
    df = engineer_features(df)
    df.to_parquet("data/transformed.parquet", index=False)
    print(f"[DAG] Transformed {len(df)} records")


with DAG(
    dag_id="iot_analytics_pipeline",
    default_args=default_args,
    description="IoT Data Pipeline — Ingest, Validate, Transform",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["data-engineering", "iot", "analytics"],
) as dag:

    ingest = PythonOperator(task_id="ingest_events", python_callable=ingest_task)
    validate = PythonOperator(task_id="validate_schema", python_callable=validate_task)
    transform = PythonOperator(task_id="transform_features", python_callable=transform_task)

    ingest >> validate >> transform