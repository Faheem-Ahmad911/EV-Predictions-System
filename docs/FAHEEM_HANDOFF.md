# Next steps for Faheem and his coding agent

Please work as Faheem-Ahmad911 in EV-Predictions-System. Moeer03 has push access
but no repository admin permission. The assignment is not yet complete; use
REPORT.md and docs/COMPLETION.md as the current audit rather than treating prior
merged PRs as proof of compliance.

1. PR #7 was approved and merged by Faheem after green CI on October 4. That
   is one distinct teammate PR review for Faheem; both members still need one
   more distinct teammate PR review. Review the current protection-audit PR
   before merging it. PR #6 remains a historical merge without prior approval.
2. dev and staging now report protected; main still reports unprotected. Enable
   main protection and verify all three branches require one approval, the three
   named CI checks, and no force pushes. Moeer03 cannot inspect detailed settings
   through the API. As administrator, preview then apply the existing script:

   ```powershell
   ./scripts/protect_branches.ps1
   ./scripts/protect_branches.ps1 -Apply
   ```

   This requires GitHub CLI installed as gh and signed in as the administrator.
   Verify one approval, all three required checks and no force pushes in GitHub.
   Confirm the instructor has collaborator access. Record a genuinely blocked
   merge with failing CI after protection is active.
3. Securely send Moeer the OAuth client JSON outside GitHub. Grant his Google
   account access to the existing Drive folder and add it to OAuth test users
   if the app is in testing. Do not send your token or .dvc/config.local.
   Preserve the storage remote and the initial dataset pointer, MD5
   5ee5ca7671e292af3ace03eddfb8031d. Confirm the dataset source URL, license and
   any sampling procedure. Moeer will authenticate with his own Google account
   and verify the exact file in a fresh clone. No separate DVC account is needed.
4. Once the shared baseline is reproducible, make your own three real experiments
   from committed code on an exp branch based on dev. Record results and promote
   the winner through a reviewed feature PR. Preserve an abandoned experiment
   branch with its rejection rationale. Do not substitute synthetic smoke scores.
5. Make a justified data-update PR into dev. Push the data to the existing DVC
   remote before Git. Have Moeer verify both old and new dataset versions. Plan
   the required two-person params conflict with Moeer; record a real rebase and
   resolution, preserving both authors' work.
6. Complete your reviews of at least two distinct Moeer PRs. Moeer must review
   another distinct Faheem PR. Prior merges without review cannot be counted as
   reviewed work. Add personal contribution and retrospective statements.
7. After real dvc.lock, metrics, experiment table and evidence are committed,
   release through reviewed dev -> staging -> main PRs. A teammate who did not
   train must independently reproduce the release from a fresh clone. Create
   model-v1.0 only after that verification and the approved main release.

Please report actual commands, hashes, scores, commit SHAs and PR/run links.
Do not mark pending checks as passed or bypass reviews to finish the checklist.
