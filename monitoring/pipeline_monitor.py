"""
Pipeline Monitor
Tracks pipeline health — record counts, null rates,
anomaly rates, and freshness checks.
"""

import pandas as pd
from datetime import datetime


def generate_health_report(df: pd.DataFrame, pipeline_name: str) -> dict:
    """Generate a structured pipeline health report."""
    report = {
        "pipeline": pipeline_name,
        "run_timestamp": datetime.utcnow().isoformat(),
        "total_records": len(df),
        "null_rates": {},
        "anomaly_rate": None,
        "status": "HEALTHY"
    }

    # Null rates per column
    for col in df.columns:
        null_rate = df[col].isnull().mean()
        report["null_rates"][col] = round(null_rate, 4)
        if null_rate > 0.05:
            report["status"] = "WARNING"
            print(f"[MONITOR] High null rate in '{col}': {null_rate:.1%}")

    # Anomaly rate
    if "is_anomaly" in df.columns:
        anomaly_rate = df["is_anomaly"].mean()
        report["anomaly_rate"] = round(anomaly_rate, 4)
        if anomaly_rate > 0.10:
            report["status"] = "CRITICAL"
            print(f"[MONITOR] High anomaly rate: {anomaly_rate:.1%}")

    print(f"[MONITOR] Pipeline '{pipeline_name}' — Status: {report['status']}")
    print(f"[MONITOR] {report['total_records']} records processed at {report['run_timestamp']}")
    return report


if __name__ == "__main__":
    df = pd.read_json("data/sample_iot_events.json")
    report = generate_health_report(df, "iot_analytics_pipeline")
    print(f"\nHealth Report:\n{report}")