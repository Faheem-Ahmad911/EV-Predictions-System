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


def clean_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw EV dataset."""
    df = df.copy()

    # Drop unique ID if present
    if "id" in df.columns:
        df = df.drop(columns=["id"])

    # Ensure target column has no missing values
    if "cost_per_kwh_usd" in df.columns:
        df = df.dropna(subset=["cost_per_kwh_usd"])

    # Fill missing values for categorical and numerical features
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown")

    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

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
    df_clean = clean_and_prepare(df)
    train_df, test_df = split_data(df_clean, test_size=test_size, random_state=seed)

    processed_dir.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(processed_dir / "train.csv", index=False)
    test_df.to_csv(processed_dir / "test.csv", index=False)
    print(
        f"Data prepared successfully: {len(train_df)} train rows, {len(test_df)} test rows saved to {processed_dir}"
    )


if __name__ == "__main__":
    prepare_dataset()
