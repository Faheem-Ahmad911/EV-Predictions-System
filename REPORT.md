# EV Predictions System - assignment progress and evidence

Audit date: October 3, 2026. Repository:
https://github.com/Faheem-Ahmad911/EV-Predictions-System

**Status: code and CI are implemented; the dataset-based release is incomplete.**
This report distinguishes completed work, historical workflow mistakes and evidence
still required. It is not a claim that model-v1.0 is ready.

## Team and sources

| Member | Ownership |
| --- | --- |
| Faheem Ahmad | Dataset, Drive/OAuth sharing, data changes, reviews, repository administration |
| Muhammad Moeer (Moeer03) | Model pipeline, notebook, CI, experiments and release coordination |

The project targets cost_per_kwh_usd in Faheem's exact initial dataset.
The committed pointer is data/raw/ev_charging_stations.csv.dvc, recording
6,943,712 bytes and its MD5. The upstream dataset URL, license and sampling
procedure still need confirmation from Faheem. The starter modules originate
in afeaec4; the team must confirm any external starter-code credit.

The earlier alternative local Kaggle sample is not used by this pipeline.
Experiments on that sample do not count as results for Faheem's dataset.

## Actual PR and merge history

| PR | Author | Route | Observed outcome |
| --- | --- | --- | --- |
| [#1](https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/1) | Faheem | feat/pre-commit -> main | Merged without a recorded teammate review; wrong feature target |
| [#2](https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/2) | Faheem | data/initial-dataset -> main | Merged; no recorded independent pull/hash review; wrong data target |
| [#3](https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/3) | Moeer | feat/moeer-assignment-completion -> main | Merged; CI passed, no recorded teammate approval; bypassed dev/staging |
| [#4](https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/4) | Faheem | main -> dev | Merged despite Moeer's unresolved changes-requested review; synchronized dev |
| [#5](https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/5) | Moeer | dev -> main | Merged; CI passed, but skipped staging and independent reproduction |
| [#6](https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/6) | Moeer | feat/moeer-workflow-compliance -> dev | Workflow corrections; red/green CI recorded; teammate review and merge pending |

main is at ca24eb5, dev at ccdcd63, and staging remains at scaffold commit
e28273d at this audit. No release tag exists. The later synchronization does not
retroactively make the earlier merges compliant. Keep this history visible.

Moeer's substantive [changes-requested review](https://github.com/Faheem-Ahmad911/EV-Predictions-System/pull/4#pullrequestreview-5400083470)
asked for accurate reporting and independent DVC verification. The inaccurate
report is corrected in the workflow-compliance feature branch. Dataset
verification remains unresolved; that review has not become an approval.

Numerical authored-merge counts are Faheem 3 and Moeer 2, but #4/#5 are
synchronization PRs. Recorded teammate-review coverage remains Faheem 0 PRs,
Moeer 1 PR. Each member must review at least two distinct teammate PRs; repeated
reviews of the same PR do not satisfy this requirement.

## Implementation and validation

- Faheem's original storage remote and raw pointer are preserved.
- prepare/train/evaluate use configs/params.yaml and a single seed. Imputation,
  encoding and scaling fit only on training data. Windows pointer discovery is fixed.
- Shared schema/range/null checks, deterministic splitting and verification tools
  are implemented. The raw CSV, model weights and OAuth credentials are not in Git.
- The EDA notebook is paired with a percent-format script and outputs are stripped.
  Execution against the exact shared dataset remains pending download.
- CI runs lint, format, tests, hooks, schema checks and synthetic smoke training.
  [PR #3 CI](https://github.com/Faheem-Ahmad911/EV-Predictions-System/actions/runs/37097204039)
  and [PR #4 CI](https://github.com/Faheem-Ahmad911/EV-Predictions-System/actions/runs/37099230916)
  passed. These use synthetic fixtures and do not prove Drive access or model quality.
- PR #6 adds a Branch policy job rejecting incorrect PR
  targets and missing release files. It also verifies that actual large-file and
  fake-secret commit attempts are rejected in a temporary repository.
- Existing local validation is recorded in docs/evidence/local-validation.md and
  docs/evidence/guardrails.txt. Updated CI evidence is described in
  docs/evidence/workflow-compliance.md.

## Reproducibility table

| Item | Current evidence |
| --- | --- |
| Shared remote | storage in .dvc/config; Google Drive |
| Initial dataset hash | MD5 recorded in data/raw/ev_charging_stations.csv.dvc; independent local verification pending |
| Dataset size | 6,943,712 bytes recorded by data owner |
| Environment | pyproject.toml + uv.lock; Python 3.14.4 |
| Parameters | seed 42; test_size 0.2; random forest, 100 trees, max_depth 10 |
| Pipeline source | dvc.yaml and src modules are committed |
| Real-data lock / metrics | dvc.lock and metrics.json are absent; no results are claimed |
| Final model and commit SHA | Pending experiments on the exact shared dataset |
| Independent reproduction | Pending a different teammate's fresh clone, dvc pull and dvc repro |
| Release tag and SHA | No model-v1.0 tag; no approved staging release |

Moeer does not yet have the OAuth client JSON. GitHub authentication as Moeer03
works, but it does not provide Google Drive authentication. Faheem must securely
share the OAuth client, grant the correct Google account access and add it as a
test user if needed. Personal tokens and .dvc/config.local must not be shared.

## Experiments and required evidence

| Requirement | Status / next action |
| --- | --- |
| Three experiments per member | Pending committed-code runs on the actual dataset; save dvc exp show tables |
| Winner promotion | Pending real measurements; apply the chosen experiment on a feature branch into dev |
| Abandoned exp branch | Prior local branches concern another sample; publish a relevant rejected experiment with rationale |
| Data-update PR / old-new recovery | Faheem must make a justified update and reviewer must restore both DVC versions |
| Two-person params conflict | Pending separate authors' changes to the same params line, rebase and recorded resolution |
| Guardrail evidence | Local rejection logs exist; CI now performs actual rejected commit attempts |
| Failed and passing CI evidence | PR #6 records actual red/green runs and screenshots in docs/evidence/workflow-compliance.md |
| Merge blocked by failed CI | Not demonstrated while branches are unprotected; repeat/check after owner protection |
| Teammate review counts | Faheem needs 2 distinct PR reviews; Moeer needs 1 more distinct PR review |
| Instructor collaborator access | Owner must confirm |
| Dataset/starter source citations | Team must confirm before final submission |

## Branch protection and release

The GitHub API still reports all three permanent branches unprotected.
Moeer03 has push/triage permissions, not admin/maintain permissions. An owner
must apply scripts/protect_branches.ps1 -Apply after the new workflow is reviewed
into dev. The script previews settings by default and refuses application without
admin permission. Required checks: Branch policy, Lint and tests, Data checks and
smoke train. Require one approval after the latest push and no force pushes.
The concrete owner/teammate handoff is in docs/FAHEEM_HANDOFF.md.

All further feature/data PRs target dev. The release then proceeds through
reviewed dev -> staging and staging -> main PRs with independent reproduction
and identical reported scores. Only then create model-v1.0. A passing synthetic
smoke test or a release-file existence check is insufficient release evidence.

## Retrospective and member contributions

Earlier feature/data merges skipped integration and staging, and a
changes-requested review did not stop a merge because branch protections were
absent. The new branch-policy check and owner protection script address recurrence;
the historical mistakes remain documented. The team must add its own retrospective
meeting conclusions and any resulting policy changes.

**Faheem:** Git history attributes the scaffold, starter modules, original tests,
guardrails, dataset pointer/Drive setup and synchronization PR to Faheem. His
personal experiments, reviews and final contribution statement remain required.

**Moeer:** Authored pipeline integration, leakage and Windows DVC fixes, EDA/CI,
verification helpers, workflow enforcement and this corrected report with assistant
support. Submitted the changes-requested review on Faheem's PR #4. His real-data
experiments, another distinct teammate review and final personal statement remain
required. These activities do not substitute for Faheem's independent work.
