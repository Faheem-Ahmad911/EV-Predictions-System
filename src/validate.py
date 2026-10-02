"""Dataset contract, shared by preparation, CI, and the EDA notebook."""

import argparse
import json

import numpy as np
import pandas as pd

CATEGORICAL = ["country", "network", "power_level", "status", "accessibility"]
RANGES = {
    "latitude": (-90, 90),
    "longitude": (-180, 180),
    "connectors_available": (1, 10000),
    "max_power_kw": (0.1, 10000),
    "install_year": (1900, 2100),
}


def validate_data(df: pd.DataFrame, target_column="cost_per_kwh_usd") -> dict:
    """Reject invalid schema/values; report imputable feature nulls explicitly."""
    required = [*CATEGORICAL, *RANGES, target_column]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if len(df) < 5:
        raise ValueError("At least five rows are required")
    for col in CATEGORICAL:
        if not df[col].dropna().map(lambda value: isinstance(value, str)).all():
            raise ValueError(f"{col} must contain strings")
    for col, (low, high) in {**RANGES, target_column: (0, 100)}.items():
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"{col} must be numeric")
        values = df[col].dropna()
        if not (np.isfinite(values).all() and values.between(low, high).all()):
            raise ValueError(f"{col} must be finite and in [{low}, {high}]")
    if df[target_column].isna().any():
        raise ValueError(f"{target_column} must not contain nulls")
    return {
        "rows": len(df),
        "duplicate_rows": int(
            df.drop(columns=["id"], errors="ignore").duplicated().sum()
        ),
        "null_counts": {col: int(df[col].isna().sum()) for col in required},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--target", default="cost_per_kwh_usd")
    args = parser.parse_args()
    print(json.dumps(validate_data(pd.read_csv(args.path), args.target), indent=2))
