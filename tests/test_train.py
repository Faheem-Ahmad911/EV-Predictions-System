"""Unit tests for model training module."""

import numpy as np
import pandas as pd
import pytest

from src.train import build_pipeline


@pytest.fixture
def dummy_train_data():
    """Create synthetic training data for model pipeline test."""
    rng = np.random.default_rng(42)
    data = {
        "country": ["United States", "Germany", "Norway", "France", "Japan"] * 10,
        "network": ["Tesla", "Ionity", "ChargePoint", "EVgo", "Electrify America"] * 10,
        "power_level": [
            "Ultra-Fast (>150kW)",
            "Level 2",
            "Level 1",
            "Level 2",
            "Ultra-Fast (>150kW)",
        ]
        * 10,
        "status": [
            "Operational",
            "Operational",
            "Under Maintenance",
            "Planned",
            "Operational",
        ]
        * 10,
        "accessibility": ["Public", "Public", "Private", "Public", "Public"] * 10,
        "latitude": rng.uniform(20.0, 60.0, 50),
        "longitude": rng.uniform(-120.0, 20.0, 50),
        "connectors_available": rng.integers(1, 10, 50),
        "max_power_kw": rng.choice([22, 50, 150, 250, 350], 50),
        "install_year": rng.choice([2020, 2021, 2022, 2023, 2024], 50),
        "cost_per_kwh_usd": rng.uniform(0.15, 0.55, 50),
    }
    return pd.DataFrame(data)


def test_build_pipeline_and_predict(dummy_train_data):
    """Test that pipeline trains and predicts valid float numbers."""
    X = dummy_train_data.drop(columns=["cost_per_kwh_usd"])
    y = dummy_train_data["cost_per_kwh_usd"]

    pipeline = build_pipeline(n_estimators=5, max_depth=3, random_state=42)
    pipeline.fit(X, y)

    predictions = pipeline.predict(X[:5])
    assert len(predictions) == 5
    assert not np.isnan(predictions).any()
