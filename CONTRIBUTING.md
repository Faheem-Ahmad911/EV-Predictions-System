# Contributing Guidelines & Team Collaboration Standards

Welcome to the **EV Predictions System** repository! This document defines the engineering standards, branching strategy, commit conventions, and review workflow for our team.

---

## 1. Branching Strategy

Our repository uses a unidirectional flow:
$$\text{feat / data / exp} \longrightarrow \text{dev} \longrightarrow \text{staging} \longrightarrow \text{main}$$

### Permanent Branches (Protected)
* `main`: Production-ready code only. Contains tagged releases (e.g., `model-v1.0`). **Direct pushes are strictly prohibited.**
* `staging`: Pre-release candidate branch. Used for full end-to-end reproducibility validation (`dvc pull` and `dvc repro`) before merging to `main`.
* `dev`: Integration branch where all reviewed feature and data branches land.

### Short-Lived Branches
* `feat/<name>`: New pipeline steps, model architecture changes, or codebase refactors. Created from `dev`, merged into `dev` via reviewed PR.
* `data/<name>`: Dataset schema or content changes tracked with DVC. **Always run `dvc push` before `git push`.**
* `exp/<member>-<idea>`: Personal exploration and hyperparameter tuning branches. These are never merged directly. If an experiment yields superior results, cherry-pick or apply it (`dvc exp apply`) onto a clean `feat/` branch.
* `fix/<name>`: Urgent production fixes branched from `main`, merged back into `main`, and then synced into `dev`.

---

## 2. Commit Message Convention

We strictly enforce **Conventional Commits**:
* `feat:` A new feature or pipeline step (e.g., `feat: add robust feature scaling in train pipeline`)
* `fix:` A bug fix (e.g., `fix: handle missing category values in data split`)
* `data:` Dataset additions or DVC pointer updates (e.g., `data: track initial 50k ev dataset sample`)
* `exp:` Model experiments and hyperparameter changes (e.g., `exp: test random forest max_depth=12`)
* `ci:` CI workflow or GitHub Actions updates (e.g., `ci: add smoke train and pytest workflow`)
* `docs:` Documentation updates (e.g., `docs: update setup instructions in README`)
* `refactor:` Code improvements without behavioral changes (e.g., `refactor: extract utils to separate module`)
* `test:` Adding or updating unit tests (e.g., `test: add unit test for target leakage`)

---

## 3. Pull Request & Merge Strategy

### Merge Decision
* **PRs into `dev`:** **Squash and Merge**. This condenses WIP commits into a single, clean Conventional Commit on `dev`, keeping history readable and traceable.
* **PRs into `staging` & `main`:** **Merge Commit** (or Fast-Forward) to preserve full release milestones and history.

### Pull Request Checklist
Every PR must use the team checklist and include:
- [ ] No data leakage (no target or future information in features)
- [ ] Splits are fixed; preprocessing fit on training data only
- [ ] No hardcoded paths; runs on any teammate's machine
- [ ] Seeds set for shuffling, initialization, and sampling
- [ ] Metric computed the way the team reports it
- [ ] `dvc push` done before `git push` (if data or models changed)
- [ ] Notebook restarted and run top to bottom (if notebooks changed)
- [ ] Style and naming: `ruff check` and `pytest` pass cleanly

## Reproducibility lessons from implementation

- Fit imputation, scaling, and encoding only within the training pipeline; never compute feature statistics before the split.
- Run `uv sync --locked` and test DVC's storage backend as well as the model dependencies. Regenerate a conflicted uv.lock from the combined pyproject.toml, then validate it.
- DVC content hashes are not credentials. Generated .dvc pointer files and dvc.lock are excluded from the secret hook, while remote configuration and source files remain scanned.
- Keep CI synthetic data/results visibly separate from real-data experiment and release results.
- A cached DVC reproduction preserves the training SHA. A forced rerun at another commit logs the new SHA; compare metrics and provenance separately rather than editing provenance to match.
- Report branch protection, approvals, experiments, and release checks only when their evidence exists. Assistant-assisted implementation does not replace the other member's independent review.
- Keep the raw-data pointer at data/raw/ev_charging_stations.csv.dvc and the shared storage remote unchanged. Do not substitute another sample when authentication fails.
- Check that `dvc dag` includes the raw pointer on Windows. A wildcard that matches an empty filename can hide a parent directory from DVC; the data/.gitignore rules and integration test prevent this regression.
