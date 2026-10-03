## What changed and why

## Metrics (before → after)

## Review checklist
- [ ] Correct target: feat/data -> dev, dev -> staging, staging -> main
- [ ] A teammate reviewed the latest commit; any changes-requested review is resolved
- [ ] No data leakage (no target or future information in features)
- [ ] Splits are fixed; preprocessing fit on training data only
- [ ] No hardcoded paths; runs on a teammate's machine
- [ ] Seeds set for shuffling, initialisation and sampling
- [ ] Metric computed the way the team reports it
- [ ] dvc push done before git push (if data or models changed)
- [ ] Notebook restarted and run top to bottom (if notebooks changed)
- [ ] Style and naming (linter passes)

## Release evidence (only for staging/main)
- [ ] dvc.lock, metrics.json and parameters refer to the shared dataset
- [ ] A teammate who did not train the final model posted fresh-clone reproduction
- [ ] Final REPORT.md links experiments, reviews, data update, conflict and screenshots
