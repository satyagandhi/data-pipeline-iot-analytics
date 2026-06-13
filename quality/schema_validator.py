"""
Schema Validator
Validates IoT event data against expected schema rules.
Flags nulls, type mismatches, and out-of-range values.
"""

import pandas as pd


REQUIRED_COLUMNS = ["device_id", "timestamp", "temperature", "pressure", "status"]
VALID_STATUSES = {"active", "alert", "inactive"}
TEMP_RANGE = (0.0, 150.0)
PRESSURE_RANGE = (80.0, 120.0)


def validate_schema(df: pd.DataFrame) -> dict:
    """Run schema validation checks and return a results report."""
    results = {
        "total_records": len(df),
        "passed": 0,
        "failed": 0,
        "issues": []
    }

    # Check required columns
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        results["issues"].append(f"Missing columns: {missing_cols}")

    # Null checks
    null_counts = df[REQUIRED_COLUMNS].isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            results["issues"].append(f"NULL values in '{col}': {count} records")

    # Value range checks
    if "temperature" in df.columns:
        out_of_range = df[
            (df["temperature"] < TEMP_RANGE[0]) |
            (df["temperature"] > TEMP_RANGE[1])
        ]
        if not out_of_range.empty:
            results["issues"].append(
                f"Temperature out of range {TEMP_RANGE}: {len(out_of_range)} records"
            )

    if "pressure" in df.columns:
        out_of_range = df[
            (df["pressure"] < PRESSURE_RANGE[0]) |
            (df["pressure"] > PRESSURE_RANGE[1])
        ]
        if not out_of_range.empty:
            results["issues"].append(
                f"Pressure out of range {PRESSURE_RANGE}: {len(out_of_range)} records"
            )

    # Status check
    if "status" in df.columns:
        invalid_status = df[~df["status"].isin(VALID_STATUSES)]
        if not invalid_status.empty:
            results["issues"].append(
                f"Invalid status values: {len(invalid_status)} records"
            )

    results["failed"] = len(results["issues"])
    results["passed"] = len(REQUIRED_COLUMNS) - results["failed"]

    for issue in results["issues"]:
        print(f"[VALIDATION FAILED] {issue}")

    if not results["issues"]:
        print("[VALIDATION PASSED] All schema checks passed.")

    return results


if __name__ == "__main__":
    import json
    df = pd.read_json("data/sample_iot_events.json")
    report = validate_schema(df)
    print(f"\nValidation Report: {report}")