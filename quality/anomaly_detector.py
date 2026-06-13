"""
Anomaly Detector
Detects statistical anomalies in IoT sensor readings
using z-score based outlier detection.
"""

import pandas as pd
import numpy as np


def detect_anomalies(df: pd.DataFrame, columns: list, threshold: float = 2.5) -> pd.DataFrame:
    """
    Flag records where sensor values deviate beyond
    the z-score threshold from the mean.
    """
    df = df.copy()
    df["is_anomaly"] = False
    df["anomaly_reason"] = ""

    for col in columns:
        if col not in df.columns:
            continue

        col_data = pd.to_numeric(df[col], errors="coerce")
        mean = col_data.mean()
        std = col_data.std()

        if std == 0:
            continue

        z_scores = (col_data - mean) / std
        anomaly_mask = z_scores.abs() > threshold

        df.loc[anomaly_mask, "is_anomaly"] = True
        df.loc[anomaly_mask, "anomaly_reason"] += f"{col} z-score={z_scores[anomaly_mask].round(2).astype(str)}; "

    anomaly_count = df["is_anomaly"].sum()
    print(f"[ANOMALY DETECTION] {anomaly_count} anomalies detected out of {len(df)} records")
    return df


if __name__ == "__main__":
    df = pd.read_json("data/sample_iot_events.json")
    result = detect_anomalies(df, columns=["temperature", "pressure"])
    print(result[result["is_anomaly"]][["device_id", "temperature", "pressure", "anomaly_reason"]])