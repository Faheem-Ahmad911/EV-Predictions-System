"""Utility functions for EV Predictions System."""

import subprocess
from pathlib import Path
from typing import Any

import yaml


def load_params(params_path: str = "configs/params.yaml") -> dict[str, Any]:
    """Load configuration parameters from a YAML file."""
    path = Path(params_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {params_path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_git_commit_sha() -> str:
    """Return the current Git commit SHA, or 'uncommitted' if unavailable."""
    try:
        output = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        )
        return output.decode("utf-8").strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "uncommitted"
