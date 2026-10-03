# EV Predictions System - assignment report

Audit date: October 3, 2026.
Repository: https://github.com/Faheem-Ahmad911/EV-Predictions-System

**Status: implementation prepared; dataset authentication, real-data execution,
collaboration evidence and release remain incomplete.** No release tag or final
model scores are claimed. See [the completion runbook](docs/COMPLETION.md).

## Team and sources

| Member | Responsibility |
| --- | --- |
| Faheem Ahmad | Dataset, shared DVC remote, hygiene, data changes and reviews |
| Moeer | Pipeline integration, EDA, CI, model experiments and release coordination |

The dataset used by this implementation is exclusively Faheem's initial
`data/raw/ev_charging_stations.csv`, represented by
`data/raw/ev_charging_stations.csv.dvc` on `data/initial-dataset`.
Faheem must confirm the upstream URL, license and subset procedure before final
submission. Starter code is the team's initial modular implementation at
`afeaec4`; confirm whether external coursework or a notebook requires credit.

The earlier local alternative Kaggle sample and experiments are not used by this
pipeline and are not counted as evidence for this dataset. Existing local files
and old experiment branches have been preserved.

## Verified implementation

Local implementation commits: `7dac9cc` (pipeline, DVC discovery, verification,
tests and environment) and `e70f963` (paired notebook and PR CI). They are on
`feat/moeer-assignment-completion`; publishing awaits the correct GitHub login.

- Incorporated Faheem's data branch through `04b6007`. The original pointer,
  expected dataset bytes and Google Drive remote remain unchanged.
- Corrected Windows pointer discovery through ignore rules, retaining the same
  nested pointer path. A DVC integration test checks discovery and execution.
- Added prepare/train/evaluate stages with code, environment and parameter
  dependencies. All paths and the single seed are in configs/params.yaml.
- Moved feature imputation into the training pipeline to prevent holdout leakage.
  Added schema/range/null checks, duplicate removal and deterministic tests.
- Added an output-free Jupytext notebook pair using tested src functions. Execution
  against Faheem's data remains pending its download.
- Added PR CI for dev/staging/main: `Lint and tests` and
  `Data checks and smoke train`. CI operates without private Drive credentials.
- Added local OAuth configuration and dataset verification commands. Secrets go
  only to ignored .dvc/config.local; verification checks hash, size and Git status.
- Installed pre-commit locally and reused the team's guardrails, aligning Ruff
  with the locked environment. Generated DVC content hashes are excluded from
  the secret hook; credentials and source code remain scanned.

## Reproducibility record

| Item | Value / status |
| --- | --- |
| Shared DVC remote | storage; exact Google Drive URL in .dvc/config |
| Dataset pointer | data/raw/ev_charging_stations.csv.dvc; unchanged from Faheem's branch |
| Dataset size | 6,943,712 bytes, as recorded by Faheem; local download pending |
| Actual local dataset MD5 | Unavailable until authenticated dvc pull succeeds |
| Environment | pyproject.toml + uv.lock; Python 3.14.4 via .python-version |
| Seed and split | 42; test_size 0.2 |
| Baseline configuration | Random forest; 100 trees; maximum depth 10 |
| Real-data dvc.lock / metrics.json | Pending; no substitute or synthetic release files committed |
| Final metrics and selected model | Pending baseline and experiments on the exact dataset |
| Independent reproduction | Pending a teammate's fresh clone and posted comparison |
| model-v1.0 tag and release SHA | Pending approved dev -> staging -> main promotion |

The DVC integration test runs in a temporary Git/DVC repository using a synthetic
fixture. It verifies stage execution, unchanged-result reuse and invalidation of
train/evaluate when a training parameter changes, without rebuilding prepare.
This validates pipeline mechanics, not Google Drive or real-data reproducibility.

Local validation: **21 tests passed**. Ruff lint/format checks passed. Notebook
pairing and stripped outputs were verified. Actual hook probes rejected a 5 MB
file and a deliberately invalid private-key fixture; neither was committed.
See [hook evidence](docs/evidence/guardrails.txt). The 300-row synthetic smoke run
completed all stages (240 training / 60 evaluation rows). Its metrics are stored
only in ignored local artifacts and are not reported as model results.

## Dataset PR review

[PR #2](https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/2) is open.
The original branch environment synced and **4 tests passed**. The CSV is ignored
and not tracked by Git. The dataset is absent locally, and a targeted DVC pull
timed out after 40 seconds with no local OAuth client configured. Approval is
pending successful authenticated download and hash verification.

The PR currently targets main; it must target dev. Windows pointer discovery
also needs the ignore-rule correction. [Draft review](docs/DATA_PR_REVIEW.md).

## Experiments and winner

No experiments on Faheem's exact dataset are claimed yet. Both members must run
at least three experiments against committed code and record `dvc exp show`
results with the dataset hash. Earlier local results on another sample are not
comparable and have not been promoted. Winner and abandonment rationale remain
pending real measurements; commands are in docs/COMPLETION.md.

## Collaboration and release evidence

| Requirement | Evidence / remaining action |
| --- | --- |
| Branches | dev, staging and main exist; API reported all unprotected on audit date |
| Protection | Owner must require PR, one approval and both CI checks; block force pushes |
| Existing guardrails PR | [PR #1](https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/1) merged into main; this differs from the required dev flow |
| Each member authors two merged PRs | Not yet evidenced; complete genuine separate contributions |
| Each member reviews two teammate PRs | Pending verification and actual reviews |
| Changes-requested review | Draft prepared; posting awaits sign-in as Moeer03 |
| Data-update PR / old-new checkout | Pending a justified update by Faheem and both-version restoration |
| Two-person parameter conflict | Pending real separate edits, rebase, resolution and linked PR |
| Abandoned experiment | Existing local branch is from different data; document a relevant rejected run |
| Guardrail screenshot | Capture actual hook rejection screenshot; logs alone are not the requested screenshot |
| Failing/passing CI screenshots | Pending actual GitHub workflow runs and enforcement |
| Release PRs and tag | No tags returned by GitHub during this audit; promotion awaits prerequisites |
| Instructor access and team roles | Repository owner must confirm |

## Retrospective observations

Feature medians computed before splitting leak evaluation information. Keeping
imputation inside the fitted model pipeline fixes this. On Windows, ignore rules
can hide a tracked nested DVC pointer from traversal; the regression test now
checks untargeted discovery. Authentication failure must not lead to substituting
datasets or reusing unrelated model scores. CONTRIBUTING.md records these lessons.
The team must add its own discussion and final conclusions before submission.

## Member contributions

**Faheem:** Git history attributes the scaffold, initial modules/tests,
documentation, guardrails and initial Google Drive dataset versioning to Faheem.
He must supply his final contribution paragraph, experiment evidence and reviews.

**Moeer:** This checkout uses Moeer03's existing Git identity. Assistant-assisted
work integrates the exact dataset setup, fixes preprocessing/discovery, and adds
notebook, pipeline, CI, verification and regression tests. Final PR/review links,
experiments and Moeer's own contribution statement remain to be completed.

The saved GitHub authentication identified a different account. Moeer confirmed
that he will sign in as Moeer03. GitHub writes remain pending that sign-in.
No teammate approvals or independent results are fabricated.
