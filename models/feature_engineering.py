"""
Feature Engineering
Transforms cleaned IoT data into ML-ready feature datasets.
"""

import pandas as pd
import numpy as np


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Generate features for downstream ML model consumption."""
    df = df.copy()

    # Time-based features
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["hour_of_day"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        df["is_business_hours"] = df["hour_of_day"].between(8, 18).astype(int)

    # Sensor ratio feature
    if "temperature" in df.columns and "pressure" in df.columns:
        df["temp_pressure_ratio"] = (
            df["temperature"] / df["pressure"].replace(0, np.nan)
        ).round(4)

    # Status encoding
    status_map = {"active": 0, "alert": 1, "inactive": 2}
    if "status" in df.columns:
        df["status_encoded"] = df["status"].map(status_map).fillna(-1).astype(int)

    # High risk flag
    if "temperature" in df.columns:
        df["high_risk_flag"] = (df["temperature"] > 100).astype(int)

    print(f"[FEATURES] {len(df.columns)} features engineered for {len(df)} records")
    return df


if __name__ == "__main__":
    df = pd.read_json("data/sample_iot_events.json")
    df = engineer_features(df)
    print(df.head())
    print(df.dtypes)