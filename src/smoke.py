"""Run the real pipeline on deterministic synthetic data, never release data."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
import yaml

from src.data import prepare_dataset
from src.evaluate import evaluate_model
from src.train import train_model
from src.validate import validate_data


def sample_data(rows=300, seed=42):
    """Create an explicitly synthetic, reproducible schema fixture for CI."""
    rng = np.random.default_rng(seed)
    power = rng.choice([22, 50, 150, 250], rows)
    return pd.DataFrame(
        {
            "id": np.arange(rows),
            "country": rng.choice(["Germany", "Norway", "United States"], rows),
            "network": rng.choice(["Tesla", "Ionity", "ChargePoint"], rows),
            "power_level": np.where(power > 150, "Ultra-Fast", "Level 2"),
            "status": ["Operational"] * rows,
            "accessibility": rng.choice(["Public", "Private"], rows),
            "latitude": rng.uniform(-60, 60, rows),
            "longitude": rng.uniform(-170, 170, rows),
            "connectors_available": rng.integers(1, 10, rows),
            "max_power_kw": power,
            "install_year": rng.integers(2018, 2026, rows),
            "cost_per_kwh_usd": 0.15 + power * 0.001 + rng.uniform(0, 0.03, rows),
        }
    )


def run_smoke(output=None):
    """Exercise all production stages in an isolated temporary directory."""
    df = sample_data()
    checks = validate_data(df)
    with TemporaryDirectory(prefix="ev-smoke-") as directory:
        root = Path(directory)
        raw = root / "sample.csv"
        df.to_csv(raw, index=False)
        params = {
            "seed": 42,
            "data": {
                "raw_path": str(raw),
                "processed_dir": str(root / "processed"),
                "target_column": "cost_per_kwh_usd",
            },
            "split": {"test_size": 0.2},
            "train": {
                "model": "random_forest",
                "n_estimators": 10,
                "max_depth": 4,
                "model_path": str(root / "model.joblib"),
            },
            "evaluate": {"metrics_file": str(root / "metrics.json")},
        }
        config = root / "params.yaml"
        config.write_text(yaml.safe_dump(params), encoding="utf-8")
        prepare_dataset(str(config))
        train_model(str(config))
        metrics = evaluate_model(str(config))
        assert all(np.isfinite(metrics[key]) for key in ["rmse", "mae", "r2"])
        result = {
            "dataset": "synthetic CI fixture; not release metrics",
            "data_checks": checks,
            "metrics": metrics,
        }
        if output:
            path = Path(output)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output")
    args = parser.parse_args()
    run_smoke(args.output)
