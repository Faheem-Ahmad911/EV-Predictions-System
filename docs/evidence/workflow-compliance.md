# Workflow correction evidence

The compliance feature branch starts from dev at ccdcd63. It adds Branch policy,
release-file checks and actual guardrail commit probes, and corrects the report.

All historical route mistakes are preserved in REPORT.md. Branch protection is
still an owner action, so a failed CI run alone is not proof that merging is blocked.

Local checks: 15 policy regression tests passed. The guardrail command attempted
real commits in a temporary repository; a 5 MB file and deliberately invalid
private-key fixture were both rejected. No fixture commit reached history.

Actual failing and passing GitHub run links and screenshots will be recorded here
when the correction PR executes. These are CI demonstrations, not dataset results.
