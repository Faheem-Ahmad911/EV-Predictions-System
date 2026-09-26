# ⚡ EV Predictions System: Git-Based MLOps & Collaboration

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/uv-fast%20packaging-green.svg)](https://github.com/astral-sh/uv)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black.svg)](https://github.com/astral-sh/ruff)
[![Testing](https://img.shields.io/badge/tests-pytest-yellow.svg)](https://pytest.org/)

A production-grade, collaborative Machine Learning repository built to predict **Electric Vehicle (EV) charging costs per kWh (`cost_per_kwh_usd`)** across global charging networks.

This project demonstrates rigorous Git collaboration, reproducible experiment tracking with **DVC**, automated code hygiene with **pre-commit hooks**, continuous integration with **GitHub Actions**, and a strict multi-tier release lifecycle (`dev` → `staging` → `main`).

---

## 🎯 Project Overview & Objective

The primary objective is that **every result is 100% reproducible by any team member or external auditor**.
* **Target Variable:** `cost_per_kwh_usd` (Continuous regression target)
* **Key Features:** Charging network, country, power level (kW), connector types, 24/7 availability, installation year, accessibility.
* **Evaluation Metrics:**
  * **RMSE** (Root Mean Squared Error)
  * **MAE** (Mean Absolute Error)
  * **$R^2$ Score** (Coefficient of Determination)

---

## 👥 Team & Ownership Roles (2-Member Team)

| Role | Primary Responsibilities | Team Member |
| :--- | :--- | :--- |
| **Data & Hygiene Owner** | DVC setup, remote storage, data validation checks, data updates, pre-commit hooks & environment pinning | Member 1 |
| **Model & Operations Owner** | Pipeline architecture, `params.yaml`, hyperparameter experiments (`dvc exp`), metrics, CI workflow & release tags | Member 2 |

---

## 📁 Repository Architecture

```text
.
├── .github/
│   ├── workflows/             # GitHub Actions CI automation (Phase 8)
│   └── pull_request_template.md # PR review checklist template
├── configs/
│   └── params.yaml            # Single source of truth for hyperparameters & paths
├── data/                      # Data storage (git-ignored, tracked via DVC)
│   ├── raw/                   # Raw CSV datasets
│   └── processed/             # Cleaned train/test splits
├── models/                    # Serialized model artifacts (.joblib, tracked via DVC)
├── notebooks/                 # Jupyter notebooks paired with Jupytext (.py:percent)
├── src/                       # Reusable, tested Python modules
│   ├── __init__.py
│   ├── utils.py               # Config loader and Git commit SHA logger
│   ├── data.py                # Data ingestion, cleaning, split without leakage
│   ├── train.py               # Model pipeline training & artifact serialization
│   └── evaluate.py            # Evaluation against test split & metrics.json output
├── tests/                     # Automated unit and integration test suite
│   ├── test_data.py
│   └── test_train.py
├── .gitignore                 # Excludes data, models, caches, and secrets
├── .pre-commit-config.yaml    # Pre-commit hooks for linting, security, and formatting
├── CONTRIBUTING.md            # Git branching rules, Conventional Commits, merge strategy
├── pyproject.toml             # Pinned project dependencies and tool configurations
├── uv.lock                    # Cryptographically locked dependency graph
├── metrics.json               # Recorded experiment metrics & git commit SHA
└── README.md                  # Project documentation & execution guide
```

---

## ⚙️ Quick Start & Developer Guide

### 1. Environment Installation
This project uses [uv](https://github.com/astral-sh/uv) for fast, deterministic dependency management.

```bash
# Clone the repository
git clone https://github.com/Faheem-Ahmad911/EV-Predictions-System.git
cd EV-Predictions-System

# Sync locked dependencies into virtual environment (.venv)
uv sync
```

### 2. Running Code Quality Checks & Tests
```bash
# Run Ruff linting check
uv run ruff check .

# Run Ruff code formatting check
uv run ruff format --check .

# Run Pytest suite
uv run pytest
```

### 3. Running the Machine Learning Pipeline
Each component is modular and can be run independently from the command line:

```bash
# 1. Prepare and split data (train/test split with fixed seed)
uv run python -m src.data

# 2. Train the model pipeline on training split only
uv run python -m src.train

# 3. Evaluate on test split and generate metrics.json
uv run python -m src.evaluate
```

---

## 🌿 Git Branching Workflow

Work flows strictly in one direction:
$$\text{feat / data / exp} \longrightarrow \text{dev} \longrightarrow \text{staging} \longrightarrow \text{main}$$

* **Never push directly to `dev`, `staging`, or `main`.**
* All changes must arrive via reviewed Pull Requests with passing CI status checks.
* For more details, see [CONTRIBUTING.md](CONTRIBUTING.md).
