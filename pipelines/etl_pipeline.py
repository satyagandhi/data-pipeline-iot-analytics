"""
ELT Pipeline
Orchestrates ingestion → validation → anomaly detection
→ transformation → feature engineering into a single run.
"""

import pandas as pd
import json
from datetime import datetime

from ingestion.stream_ingestor import ingest_events, normalise_schema
from quality.schema_validator import validate_schema
from quality.anomaly_detector import detect_anomalies
from models.feature_engineering import engineer_features


def run_pipeline(input_path: str, output_path: str) -> pd.DataFrame:
    """Execute the full ELT pipeline end-to-end."""
    print(f"\n{'='*50}")
    print(f"Pipeline Run: {datetime.utcnow().isoformat()}")
    print(f"{'='*50}\n")

    # Step 1 — Ingest
    df = ingest_events(input_path)
    df = normalise_schema(df)

    # Step 2 — Validate
    validation_report = validate_schema(df)
    if validation_report["failed"] > 0:
        print(f"[PIPELINE] Warning: {validation_report['failed']} validation issues found")

    # Step 3 — Anomaly Detection
    df = detect_anomalies(df, columns=["temperature", "pressure"])

    # Step 4 — Feature Engineering
    df = engineer_features(df)

    # Step 5 — Output
    df.to_csv(output_path, index=False)
    print(f"\n[PIPELINE] Complete. {len(df)} records written to {output_path}")
    return df


if __name__ == "__main__":
    run_pipeline(
        input_path="data/sample_iot_events.json",
        output_path="data/pipeline_output.csv"
    )