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
| **Data & Hygiene Owner** | DVC setup, remote storage, data validation checks, data updates, pre-commit hooks & environment pinning | Faheem Ahmad |
| **Model & Operations Owner** | Pipeline architecture, `params.yaml`, hyperparameter experiments (`dvc exp`), metrics, CI workflow & release tags | Moeer |

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

---

## Current Collaboration Handoff

This section records the work completed by **Faheem** and the exact checks that
**Moeer** must perform before reviewing the data pull request. It is intended to
make the repository state and ownership visible to both team members.

### Work completed by Faheem

Faheem prepared the initial project foundation, including:

- the standard ML repository structure;
- reusable data preparation, training, evaluation, and utility modules in
  `src/`;
- unit tests for data preparation and model training;
- centralized model and split parameters in `configs/params.yaml`;
- a pinned `uv` environment using `pyproject.toml` and `uv.lock`;
- project documentation, contribution rules, branch naming, Conventional
  Commits, and the pull-request checklist;
- pre-commit guard rails for Ruff linting/formatting, notebook output removal,
  YAML/JSON checks, files larger than 1 MB, and secret detection.

### Initial dataset versioning completed by Faheem

The initial EV charging dataset was versioned on the
`data/initial-dataset` branch.

The following work was completed:

1. DVC and its Google Drive extension were added to the locked project
   environment.
2. DVC was initialized in the Git repository.
3. A shared Google Drive folder was configured as the default DVC remote named
   `storage`.
4. The raw dataset was added to DVC at:

   ```text
   data/raw/ev_charging_stations.csv
   ```

5. Git tracks only the pointer file:

   ```text
   data/raw/ev_charging_stations.csv.dvc
   ```

6. The raw CSV remains ignored by Git and is therefore not stored in GitHub
   history.
7. The pointer records this verified dataset metadata:

   ```text
   MD5: 5ee5ca7671e292af3ace03eddfb8031d
   Size: 6,943,712 bytes
   ```

8. The dataset object was uploaded successfully to the shared Google Drive
   remote (`1 file pushed`).
9. The Google Drive authentication dependency was updated to a current
   `pyOpenSSL` release compatible with the locked `cryptography` package.
10. OAuth credentials were saved only in `.dvc/config.local`. This file is
    ignored by Git; no client secret, access token, or user credential is
    committed to the repository.

### Commits on the data branch

The data branch contains these Faheem-authored commits:

```text
690b630 data: version initial dataset with DVC and Google Drive
c7a611f fix: update Google Drive authentication dependency
```

### Required review by Moeer

Moeer must not approve the data pull request from the GitHub diff alone. He
must verify the remote from a fresh checkout.

1. Update or clone the repository and check out the data branch:

   ```bash
   git fetch origin
   git switch --track origin/data/initial-dataset
   ```

   If the local branch already exists:

   ```bash
   git switch data/initial-dataset
   git pull origin data/initial-dataset
   ```

2. Install the exact locked environment:

   ```bash
   uv sync
   ```

3. Confirm the raw CSV is not present before pulling, if testing from a clean
   clone.
4. Run:

   ```bash
   uv run dvc pull
   ```

5. Complete Google authorization using Moeer's own Google account. Moeer must
   have access to the shared Drive folder and must never receive Faheem's local
   OAuth token or `.dvc/config.local` file.
6. Verify the downloaded file:

   ```powershell
   Test-Path data/raw/ev_charging_stations.csv
   Get-FileHash -Algorithm MD5 data/raw/ev_charging_stations.csv
   ```

7. The expected results are:

   ```text
   File exists: True
   MD5: 5EE5CA7671E292AF3ACE03EDDFB8031D
   ```

8. Run the existing tests:

   ```bash
   uv run pytest
   ```

9. Confirm that the CSV is not tracked by Git:

   ```bash
   git check-ignore data/raw/ev_charging_stations.csv
   git ls-files data/raw/ev_charging_stations.csv
   ```

   The first command should report the ignored CSV path. The second command
   should print nothing.
10. Post the DVC pull result, hash verification, and test result in the pull
    request review before approving it.

### Security rules for both members

- Never commit `.dvc/config.local`, OAuth JSON files, Google access tokens, or
  downloaded client-secret files.
- Never add the raw CSV using `git add`.
- Run `uv run dvc push` before `git push` whenever DVC-tracked data or models
  change.
- Each member must authenticate using their own Google account.
- Both members must preserve their own commits, pull requests, and review
  history because individual contribution is part of the assignment grade.

### Current next action

Faheem must open the `data/initial-dataset` pull request into `dev` and assign
Moeer as reviewer. Moeer must complete the verification above before the branch
is merged.
