"""Reject the PR paths that previously bypassed integration and staging."""

import json

import pytest

from scripts.check_pr_policy import branch_error, check_event, release_errors


@pytest.mark.parametrize(
    "head,base",
    [
        ("feat/eda", "dev"),
        ("data/update", "dev"),
        ("dev", "staging"),
        ("staging", "main"),
        ("fix/bug", "main"),
    ],
)
def test_allowed_branch_paths(head, base):
    assert branch_error(head, base) is None


@pytest.mark.parametrize(
    "head,base",
    [
        ("feat/eda", "main"),
        ("data/initial-dataset", "main"),
        ("dev", "main"),
        ("exp/moeer-tuning", "dev"),
        ("main", "dev"),
        ("feat/", "dev"),
    ],
)
def test_shortcuts_rejected(head, base):
    assert branch_error(head, base)


def test_recovery_requires_explicit_label():
    assert branch_error("main", "dev", ["workflow-recovery"]) is None
    assert branch_error("main", "dev", ["hotfix-sync"]) is None
    assert branch_error("dev", "main", ["workflow-recovery"])


def test_release_requires_pipeline_evidence(tmp_path):
    event = {"pull_request": {"head": {"ref": "dev"}, "base": {"ref": "staging"}}}
    errors = check_event(event, tmp_path)
    assert "Missing release evidence: dvc.lock" in errors
    assert "Missing release evidence: metrics.json" in errors


def test_feature_work_does_not_claim_release_readiness(tmp_path):
    event = {"pull_request": {"head": {"ref": "feat/work"}, "base": {"ref": "dev"}}}
    assert check_event(event, tmp_path) == []


def test_invalid_release_metrics_rejected(tmp_path):
    (tmp_path / "metrics.json").write_text(
        json.dumps({"rmse": True, "mae": -1, "r2": None})
    )
    errors = release_errors(tmp_path)
    assert any("finite numeric rmse" in error for error in errors)
    assert any("nonnegative" in error for error in errors)
    assert any("commit SHA" in error for error in errors)
