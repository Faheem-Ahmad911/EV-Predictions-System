"""Data-contract and leakage regression tests."""

import numpy as np
import pytest

from src.data import clean_and_prepare, split_data
from src.smoke import run_smoke, sample_data
from src.train import build_pipeline
from src.validate import validate_data


@pytest.mark.parametrize(
    "column,value",
    [
        ("latitude", 91),
        ("longitude", -181),
        ("max_power_kw", -1),
        ("cost_per_kwh_usd", -0.1),
        ("cost_per_kwh_usd", np.nan),
        ("connectors_available", np.inf),
    ],
)
def test_invalid_values_rejected(column, value):
    df = sample_data(20)
    df[column] = df[column].astype(float)
    df.loc[0, column] = value
    with pytest.raises(ValueError, match=column):
        validate_data(df)


def test_schema_rejected():
    with pytest.raises(ValueError, match="country"):
        validate_data(sample_data().drop(columns="country"))


def test_cleaning_preserves_nulls_for_training_only_imputation():
    df = sample_data(20)
    df.loc[0, "latitude"] = np.nan
    cleaned = clean_and_prepare(df)
    assert np.isnan(cleaned.loc[0, "latitude"])
    assert validate_data(df)["null_counts"]["latitude"] == 1


def test_imputer_uses_only_training_median_and_handles_unseen_categories():
    train = sample_data(20)
    train["latitude"] = 10.0
    train.loc[0, "latitude"] = np.nan
    X = train.drop(columns="cost_per_kwh_usd")
    model = build_pipeline(n_estimators=5)
    model.fit(X, train["cost_per_kwh_usd"])
    numeric = model.named_steps["preprocessor"].named_transformers_["num"]
    assert numeric.named_steps["imputer"].statistics_[0] == 10.0
    test = X.iloc[:2].copy()
    test["country"] = "unseen-country"
    test["latitude"] = [np.nan, 89.0]
    assert np.isfinite(model.predict(test)).all()
    assert numeric.named_steps["imputer"].statistics_[0] == 10.0


def test_split_is_reproducible_and_disjoint():
    df = sample_data()
    a, b = split_data(df)
    c, d = split_data(df)
    assert a.equals(c) and b.equals(d)
    assert set(a.index).isdisjoint(b.index)


def test_pipeline_end_to_end():
    result = run_smoke()
    assert result["metrics"]["n_test_samples"] == 60
    assert result["metrics"]["rmse"] < 0.05
