# Next steps in the instructor's order

1. Faheem (repository owner) securely supplies the OAuth client JSON, verifies
   Moeer's Google account can access the Drive folder and OAuth project, and
   confirms dataset source URL/license and subset procedure. Keep the existing
   pointer and storage remote.
2. Moeer runs the configure_drive and verify_dataset commands from README in a
   fresh checkout. Record the actual dvc pull output and matching MD5. Then execute
   the notebook and real pipeline, commit dvc.lock/metrics.json, dvc push, and open
   a feature PR into dev. Do not substitute the older local Kaggle sample.
3. PR #6 has already merged into dev without a recorded review. Faheem reviews
   the current audit-correction PR and future feature PRs before they merge.
   No direct feature or dev PR goes into main.
4. The owner applies scripts/protect_branches.ps1 -Apply (preview without -Apply).
   This requires GitHub admin access; Moeer03 currently has push access only.
   Verify both approvals and failed required checks actually block merging.
5. Both members run at least three experiments from committed code on their own
   exp branches created from dev. Save dvc exp show, data hash and rationale. Promote
   winners to feat branches with reviewed PRs; preserve a rejected exp branch.
6. Faheem authors a justified data-update PR into dev. Moeer verifies git checkout
   plus dvc checkout restores old and new versions. Record real hashes and reviews.
7. Both members independently change the same params line on separate branches.
   After the first reviewed merge, the second author rebases on dev, resolves the
   real conflict, reproduces the pipeline and documents the resolution.
8. Each member reviews at least two distinct teammate PRs. A merged PR or a review
   of one's own work does not count as independent teammate review. Resolve the
   actual changes-requested review before claiming approval.
9. Update REPORT.md with final facts, source citations, member statements,
   experiment tables and actual screenshot/PR links. The initial wrong merge
   routes remain acknowledged in the history.
10. Open dev -> staging as release: v1.0. A teammate who did not train the final
    model clones fresh, pulls DVC artifacts, reproduces and posts exact metrics.
    After approval, merge staging; then open and approve staging -> main. Tag
    model-v1.0 on that final main commit. Do not tag the current incomplete model.

## Commands after the OAuth client arrives

```powershell
uv sync --locked
uv run python -m src.configure_drive "C:/outside-repo/client.json"
uv run dvc pull
uv run python -m src.verify_dataset
uv run dvc repro
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01-eda.ipynb
uv run nbstripout notebooks/01-eda.ipynb
uv run jupytext --sync notebooks/01-eda.ipynb
uv run dvc push
```

Record outputs against committed code and the exact initial pointer. Cached
reproduction preserves the original commit SHA; forced recomputation at a later
commit may log a new SHA. Never edit provenance to manufacture identical results.

## Example experiments after a reviewed baseline reaches dev

```powershell
git switch -c exp/moeer-dvc-tuning origin/dev
uv run dvc exp run -n moeer-initial-50 --set-param configs/params.yaml:train.n_estimators=50
uv run dvc exp run -n moeer-initial-100 --set-param configs/params.yaml:train.n_estimators=100
uv run dvc exp run -n moeer-initial-200 --set-param configs/params.yaml:train.n_estimators=200
uv run dvc exp show
```

Faheem runs and records his own three variants. Select a winner using actual
RMSE/MAE/R2 and model cost. Repeatedly tuning on a holdout is a course exercise;
it does not produce an unbiased estimate of final model performance.
