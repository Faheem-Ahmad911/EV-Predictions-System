# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # EV charging costs: exploratory analysis
# Run `uv run dvc pull` from the repository root before running all cells.
# This notebook uses the actual DVC dataset; CI fixtures are not research data.
# All learned preprocessing is fitted on training data inside `src.train`.

# %%
import sys
from pathlib import Path

ROOT = Path.cwd()
if not (ROOT / "configs/params.yaml").exists():
    ROOT = ROOT.parent
if not (ROOT / "configs/params.yaml").exists():
    raise RuntimeError("Open this notebook from the repository or notebooks directory")
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt

from src.data import clean_and_prepare, load_raw_data
from src.utils import load_params
from src.validate import validate_data

params = load_params(str(ROOT / "configs/params.yaml"))
target = params["data"]["target_column"]
raw = load_raw_data(str(ROOT / params["data"]["raw_path"]))
checks = validate_data(raw, target)
print(checks)

# %% [markdown]
# ## Overview and missingness
# Validation checks schema, finite numeric values and permitted ranges. Feature
# nulls are reported and retained for training-only imputation. Missing targets
# fail the raw-data contract and must be corrected by the data owner.

# %%
print(f"Rows: {len(raw):,}; columns: {raw.shape[1]}")
print(raw.dtypes)
raw.head()

# %%
raw.isna().sum().sort_values(ascending=False).plot.bar(title="Missing values by column")
plt.ylabel("Rows")
plt.tight_layout()
plt.show()

# %%
clean = clean_and_prepare(raw, target)
print(f"Removed {len(raw) - len(clean)} duplicate or missing-target rows")
clean.describe(include="all")

# %% [markdown]
# ## Target distribution and feature relationships
# Associations here are descriptive, not evidence of causal effects or model
# performance. Final model selection must use reproducible experiment results.

# %%
clean[target].plot.hist(bins=40, title="Charging cost distribution")
plt.xlabel("USD per kWh")
plt.tight_layout()
plt.show()

# %%
clean.groupby("network")[target].mean().sort_values().plot.barh(
    title="Mean charging cost by network"
)
plt.xlabel("USD per kWh")
plt.tight_layout()
plt.show()

# %%
sample = clean.sample(min(2000, len(clean)), random_state=params["seed"])
sample.plot.scatter(
    x="max_power_kw",
    y=target,
    alpha=0.25,
    title="Power and charging cost (seeded sample)",
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Modeling decisions
# Remove IDs and identical rows before splitting. Preserve feature nulls until
# the training pipeline fits imputers. Use the configured seed and holdout ratio.
# Record observed conclusions only after executing against the versioned dataset.
