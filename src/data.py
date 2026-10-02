"""Data preparation and preprocessing module for EV Predictions System."""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

try:
    from src.utils import load_params
except ImportError:
    from utils import load_params


def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load raw dataset from CSV."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {filepath}")
    return pd.read_csv(path)


def clean_and_prepare(
    df: pd.DataFrame, target_column: str = "cost_per_kwh_usd"
) -> pd.DataFrame:
    """Clean the raw EV dataset."""
    df = df.copy()

    # Drop unique ID if present
    if "id" in df.columns:
        df = df.drop(columns=["id"])

    # Ensure target column has no missing values
    if target_column not in df.columns:
        raise ValueError(f"Missing target column: {target_column}")
    df = df.dropna(subset=[target_column])
    # Feature imputation belongs inside the fitted training pipeline.
    # Remove identical records before splitting to avoid cross-split duplicates.
    df = df.drop_duplicates()

    return df


def split_data(
    df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split data into train and test sets with fixed random seed."""
    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=random_state
    )
    return train_df, test_df


def prepare_dataset(params_path: str = "configs/params.yaml") -> None:
    """Main pipeline function to load, clean, split, and save data."""
    params = load_params(params_path)
    raw_path = params["data"]["raw_path"]
    processed_dir = Path(params["data"]["processed_dir"])
    test_size = params["split"]["test_size"]
    seed = params["seed"]

    df = load_raw_data(raw_path)
    from src.validate import validate_data

    validate_data(df, target_column=params["data"]["target_column"])
    df_clean = clean_and_prepare(df, params["data"]["target_column"])
    train_df, test_df = split_data(df_clean, test_size=test_size, random_state=seed)

    processed_dir.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(processed_dir / "train.csv", index=False, lineterminator="\n")
    test_df.to_csv(processed_dir / "test.csv", index=False, lineterminator="\n")
    print(
        f"Data prepared successfully: {len(train_df)} train rows, {len(test_df)} test rows saved to {processed_dir}"
    )


if __name__ == "__main__":
    prepare_dataset()
