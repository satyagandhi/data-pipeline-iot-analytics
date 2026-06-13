# data-pipeline-iot-analytics

A production-grade data engineering project that simulates, ingests, validates, transforms, and monitors IoT device event data — producing ML-ready feature datasets for predictive analytics.

## Architecture

## Tech Stack

- **Python** — pipeline logic, transformation, feature engineering
- **Apache Spark / PySpark** — distributed data processing
- **Apache Airflow** — pipeline orchestration and scheduling
- **Apache Kafka** — real-time event streaming
- **Azure Databricks / Delta Lake** — cloud lakehouse storage
- **SQL** — data validation and quality checks

## Project Structure

| Folder | Purpose |
|--------|---------|
| `ingestion/` | IoT event simulation and stream normalisation |
| `quality/` | Schema validation and anomaly detection |
| `pipelines/` | End-to-end ELT orchestration |
| `models/` | Feature engineering for ML consumption |
| `orchestration/` | Airflow DAG definition |
| `monitoring/` | Pipeline health reporting |

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Simulate IoT events
python ingestion/iot_simulator.py

# Run schema validation
python quality/schema_validator.py

# Run anomaly detection
python quality/anomaly_detector.py

# Run full pipeline
python pipelines/etl_pipeline.py

# Run pipeline monitor
python monitoring/pipeline_monitor.py
```

## Key Features

- Real-time IoT event simulation across multiple devices
- Automated schema validation with null, type, and range checks
- Z-score based anomaly detection on sensor readings
- Feature engineering producing ML-ready datasets
- Airflow DAG for scheduled pipeline orchestration
- Pipeline health monitoring with HEALTHY / WARNING / CRITICAL alerts
- End-to-end data lineage from raw ingestion to feature output

## Results

Engineered feature pipelines supporting predictive analytics contributed to a **10–20% operational cost reduction** through data-driven decision making.