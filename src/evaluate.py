"""Model evaluation module for EV Predictions System."""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

try:
    from src.utils import get_git_commit_sha, load_params
except ImportError:
    from utils import get_git_commit_sha, load_params


def evaluate_model(params_path: str = "configs/params.yaml") -> dict:
    """Evaluate trained model on test split and save metrics.json."""
    params = load_params(params_path)
    processed_dir = Path(params["data"]["processed_dir"])
    target_col = params["data"]["target_column"]
    test_file = processed_dir / "test.csv"
    model_path = Path(params["train"]["model_path"])
    metrics_file = Path(params["evaluate"]["metrics_file"])

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run src/train.py first."
        )
    if not test_file.exists():
        raise FileNotFoundError(
            f"Test data not found at {test_file}. Run src/data.py first."
        )

    pipeline = joblib.load(model_path)
    test_df = pd.read_csv(test_file)

    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]

    predictions = pipeline.predict(X_test)

    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    mae = float(mean_absolute_error(y_test, predictions))
    r2 = float(r2_score(y_test, predictions))
    commit_sha = get_git_commit_sha()

    metrics = {
        "commit_sha": commit_sha,
        "rmse": round(rmse, 4),
        "mae": round(mae, 4),
        "r2": round(r2, 4),
        "n_test_samples": len(y_test),
        "n_estimators": params["train"]["n_estimators"],
        "max_depth": params["train"]["max_depth"],
        "seed": params["seed"],
    }

    metrics_file.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        f.write("\n")

    print("Evaluation Results:")
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    evaluate_model()
