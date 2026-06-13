"""
Stream Ingestor
Ingests IoT event streams and normalises nested,
semi-structured data into a consistent schema.
"""

import json
import pandas as pd
from datetime import datetime


EXPECTED_SCHEMA = {
    "device_id": str,
    "timestamp": str,
    "temperature": float,
    "pressure": float,
    "status": str,
    "location": str
}

VALID_STATUSES = {"active", "alert", "inactive"}


def ingest_events(filepath: str) -> pd.DataFrame:
    """Load raw IoT events and normalise into a flat DataFrame."""
    with open(filepath, "r") as f:
        raw_events = json.load(f)

    df = pd.json_normalize(raw_events)
    print(f"[INGEST] Loaded {len(df)} raw events")
    return df


def normalise_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Enforce consistent schema and column types."""
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["pressure"] = pd.to_numeric(df["pressure"], errors="coerce")
    df["status"] = df["status"].str.lower().str.strip()
    df["ingested_at"] = datetime.utcnow()

    if "location" not in df.columns:
        df["location"] = "unknown"

    print(f"[INGEST] Schema normalised — {len(df)} records")
    return df


if __name__ == "__main__":
    df = ingest_events("data/sample_iot_events.json")
    df = normalise_schema(df)
    print(df.dtypes)
    print(df.head())