"""Model training pipeline for EV Predictions System."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    from src.utils import load_params
except ImportError:
    from utils import load_params


def build_pipeline(
    n_estimators: int = 100, max_depth: int = 10, random_state: int = 42
) -> Pipeline:
    """Build preprocessing and modeling pipeline."""
    categorical_features = [
        "country",
        "network",
        "power_level",
        "status",
        "accessibility",
    ]
    numeric_features = [
        "latitude",
        "longitude",
        "connectors_available",
        "max_power_kw",
        "install_year",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
            ("num", StandardScaler(), numeric_features),
        ],
        remainder="drop",
    )

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        n_jobs=-1,
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("regressor", model)])


def train_model(params_path: str = "configs/params.yaml") -> None:
    """Train the model and save the fitted pipeline artifact."""
    params = load_params(params_path)
    processed_dir = Path(params["data"]["processed_dir"])
    target_col = params["data"]["target_column"]
    train_file = processed_dir / "train.csv"

    if not train_file.exists():
        raise FileNotFoundError(
            f"Train file not found at {train_file}. Run src/data.py first."
        )

    train_df = pd.read_csv(train_file)
    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]

    n_estimators = params["train"]["n_estimators"]
    max_depth = params["train"]["max_depth"]
    seed = params["seed"]

    pipeline = build_pipeline(
        n_estimators=n_estimators, max_depth=max_depth, random_state=seed
    )

    print(
        f"Training model with n_estimators={n_estimators}, max_depth={max_depth}, seed={seed}..."
    )
    pipeline.fit(X_train, y_train)

    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "model.joblib"
    joblib.dump(pipeline, model_path)
    print(f"Model saved successfully to {model_path}")


if __name__ == "__main__":
    train_model()
