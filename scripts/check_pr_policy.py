"""Check assignment branch flow and minimum release evidence for a pull request."""

import argparse
import json
import math
import os
import re
from pathlib import Path


def branch_error(head, base, labels=()):
    """Return a useful error for a PR that skips the assignment's branch flow."""
    if base == "dev" and re.fullmatch(r"(?:feat|data)/.+", head):
        return None
    if (head, base) in {("dev", "staging"), ("staging", "main")}:
        return None
    if base == "main" and re.fullmatch(r"fix/.+", head):
        return None
    if (head, base) == ("main", "dev") and set(labels) & {
        "hotfix-sync",
        "workflow-recovery",
    }:
        return None
    return (
        f"PR {head} -> {base} skips the required branch flow. "
        "Use feat/* or data/* -> dev -> staging -> main. "
        "Hotfixes use fix/* -> main. A main -> dev synchronization needs "
        "the hotfix-sync or workflow-recovery label and a documented reason. "
        "Promote experiment results onto a feature branch; do not merge exp/* directly."
    )


def release_errors(root):
    """Require committed release evidence; this does not prove reproduction."""
    required = [
        "dvc.yaml",
        "dvc.lock",
        "metrics.json",
        "configs/params.yaml",
        "uv.lock",
        "data/raw/ev_charging_stations.csv.dvc",
    ]
    errors = [
        f"Missing release evidence: {name}"
        for name in required
        if not (root / name).is_file()
    ]
    if not (root / "metrics.json").is_file():
        return errors
    try:
        metrics = json.loads((root / "metrics.json").read_text(encoding="utf-8"))
        if not isinstance(metrics, dict):
            raise TypeError("expected an object")
        for key in ["rmse", "mae", "r2"]:
            value = metrics.get(key)
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                errors.append(f"metrics.json must contain a finite numeric {key}")
            elif key != "r2" and value < 0:
                errors.append(f"metrics.json {key} must be nonnegative")
        if not re.fullmatch(r"[0-9a-f]{40}", str(metrics.get("commit_sha", ""))):
            errors.append("metrics.json needs the full training/evaluation commit SHA")
    except (ValueError, TypeError, OSError) as exc:
        errors.append(f"Cannot read metrics.json: {exc}")
    return errors


def check_event(event, root):
    pr = event.get("pull_request")
    if pr is None:
        raise ValueError("A pull_request event is required")
    head, base = pr["head"]["ref"], pr["base"]["ref"]
    error = branch_error(head, base, [label["name"] for label in pr.get("labels", [])])
    errors = [error] if error else []
    if base in {"staging", "main"}:
        errors.extend(release_errors(root))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", default=os.environ.get("GITHUB_EVENT_PATH"))
    args = parser.parse_args()
    if not args.event:
        parser.error("--event or GITHUB_EVENT_PATH is required")
    event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    errors = check_event(event, Path.cwd())
    for error in errors:
        print(error)
    if errors:
        return 1
    print("PR branch flow and applicable release-file checks passed.")
    print("Teammate approval and independent DVC reproduction remain required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
