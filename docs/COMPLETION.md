# Assignment completion runbook

This runbook records the remaining steps; it is not evidence that they happened.

## 1. Verify and review Faheem's dataset

PR #2: https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/2

- Change the PR base from main to dev.
- Use your own Google account, with shared-folder and OAuth test-user access.
- Configure the securely supplied OAuth client JSON using `python -m src.configure_drive`.
- From a fresh checkout of the corrected data branch, run `uv sync --locked`,
  `uv run dvc pull`, `uv run python -m src.verify_dataset`, and `uv run pytest`.
  The verification helper is on the completion branch; on the original data
  branch use Faheem's Test-Path/Get-FileHash/check-ignore/ls-files commands.
- Confirm DVC discovers the raw pointer with `uv run dvc dag`. The completion
  branch fixes a Windows ignore-rule discovery problem without changing it.
- Post the actual pull output, MD5, tests, and Git checks. The draft review in
  `docs/DATA_PR_REVIEW.md` describes what has and has not been verified.

## 2. Establish the actual baseline

```powershell
uv run dvc pull
uv run python -m src.verify_dataset
uv run dvc repro
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01-eda.ipynb
uv run nbstripout notebooks/01-eda.ipynb
uv run jupytext --sync notebooks/01-eda.ipynb
uv run dvc push
git add dvc.lock metrics.json notebooks
git commit -m "feat: record verified dataset baseline"
```

Use committed implementation code for the baseline and experiments. Preserve
Faheem's raw file, nested pointer, and storage remote. Local files from older
experiments against other data are not release evidence. The current pipeline
does not consume those files.

## 3. Experiments and promotion

Once the baseline is reviewed into dev, each member creates their own experiment
branch from updated dev and runs at least three experiments on committed code.
For Moeer:

```powershell
git switch -c exp/moeer-dvc-tuning origin/dev
uv run dvc exp run -n moeer-initial-50 --set-param configs/params.yaml:train.n_estimators=50
uv run dvc exp run -n moeer-initial-100 --set-param configs/params.yaml:train.n_estimators=100
uv run dvc exp run -n moeer-initial-200 --set-param configs/params.yaml:train.n_estimators=200
uv run dvc exp show
```

Faheem independently runs his own three variants. Save the actual tables in
REPORT.md with the dataset hash. Compare RMSE, MAE, R2 and model size; do not
assume any particular configuration wins. Repeated holdout-based selection is
an assignment exercise, not an unbiased final performance estimate.

Apply the selected experiment to a clean feat branch with `dvc exp apply`,
reproduce, upload artifacts with `dvc push`, then commit/push and open a reviewed
PR into dev. Preserve an abandoned experiment branch and explain its rejection.

## 4. Required team evidence

- Both members: at least two authored merged PRs and two teammate reviews.
  Use separate meaningful PRs for notebook/CI/pipeline changes as appropriate.
- Record a substantive changes-requested review and its resolution.
- Data owner: make a justified data update, `dvc add` the same raw path and
  `dvc push` before Git push. Demonstrate git checkout plus dvc checkout restoring
  old and new dataset hashes. Never alter the initial pointer just to unblock a pull.
- Both members edit the same params line on separate branches; after the first
  reviewed merge, the second author rebases, resolves the real conflict and tests.
- Capture actual hook rejection and failing/passing CI screenshots. A synthetic
  smoke run is not a GitHub Actions result or a screenshot.
- Repository owner: add the instructor, require one approval and both named CI
  checks on dev/staging/main, and block force pushes.
- Confirm upstream dataset URL/license and starter-code provenance in REPORT.md.

## 5. Reviewed release

Open dev -> staging titled `release: v1.0`. Faheem (or a teammate who did not train
the final model) must clone fresh, switch to the proposed release revision,
run `uv sync --locked`, `uv run dvc pull`, and `uv run dvc repro`, then post the
exact metrics.json comparison. Cached reproduction preserves the original
training SHA. Forced recomputation at another commit changes provenance; never
edit SHA fields to make files appear equal.

After successful reproduction and approval, merge into staging; open and obtain
approval for staging -> main. Only after that merge:

```powershell
git switch main
git pull --ff-only
git tag -a model-v1.0 -m "First production model"
git push origin model-v1.0
```

Complete REPORT.md with real PR/review links, experiment results, screenshots,
tag SHA, lock/metrics and member-written retrospective/contribution paragraphs.
