"""Unit tests for data preparation module."""

import pandas as pd
import pytest

from src.data import clean_and_prepare, split_data


@pytest.fixture
def sample_dataframe():
    """Create a minimal synthetic dataframe matching EV stations structure."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "country": [
                "United States",
                "Germany",
                "Norway",
                "United States",
                "Germany",
            ],
            "city": ["Austin", "Berlin", "Oslo", "Dallas", "Munich"],
            "network": ["Tesla", "Ionity", "ChargePoint", "Tesla", "Ionity"],
            "latitude": [30.26, 52.52, 59.91, 32.77, 48.13],
            "longitude": [-97.74, 13.40, 10.75, -96.79, 11.58],
            "connectors_available": [4, 6, 2, 8, 4],
            "connector_types": ["Tesla NACS", "CCS", "Type 2", "Tesla NACS", "CCS"],
            "power_level": [
                "Ultra-Fast (>150kW)",
                "Level 2",
                "Level 1",
                "Ultra-Fast (>150kW)",
                "Level 2",
            ],
            "max_power_kw": [250, 50, 22, 250, 50],
            "is_24_7": [True, True, False, True, True],
            "cost_per_kwh_usd": [0.28, 0.45, 0.20, 0.30, 0.42],
            "status": [
                "Operational",
                "Operational",
                "Under Maintenance",
                "Operational",
                "Operational",
            ],
            "install_year": [2023, 2022, 2021, 2024, 2023],
            "accessibility": ["Public", "Public", "Private", "Public", "Public"],
        }
    )


def test_clean_and_prepare_drops_id(sample_dataframe):
    """Test that ID column is dropped during preparation."""
    cleaned = clean_and_prepare(sample_dataframe)
    assert "id" not in cleaned.columns


def test_clean_and_prepare_no_missing_target(sample_dataframe):
    """Test that missing target rows are removed."""
    df_with_nan = sample_dataframe.copy()
    df_with_nan.loc[0, "cost_per_kwh_usd"] = None
    cleaned = clean_and_prepare(df_with_nan)
    assert len(cleaned) == len(sample_dataframe) - 1
    assert cleaned["cost_per_kwh_usd"].isna().sum() == 0


def test_split_data_ratio(sample_dataframe):
    """Test that split preserves specified ratio."""
    train_df, test_df = split_data(sample_dataframe, test_size=0.4, random_state=42)
    assert len(train_df) == 3
    assert len(test_df) == 2
