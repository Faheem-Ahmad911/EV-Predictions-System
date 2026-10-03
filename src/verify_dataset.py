"""Verify the local dataset against Faheem's committed DVC pointer."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import yaml

from src.data import load_raw_data
from src.validate import validate_data


def verify_dataset(pointer="data/raw/ev_charging_stations.csv.dvc"):
    pointer = Path(pointer)
    metadata = yaml.safe_load(pointer.read_text(encoding="utf-8"))["outs"][0]
    raw = pointer.parent / metadata["path"]
    if not raw.is_file():
        raise FileNotFoundError(f"Dataset missing: {raw}. Run uv run dvc pull first.")
    with raw.open("rb") as stream:
        actual = hashlib.file_digest(stream, "md5").hexdigest()
    if actual != metadata["md5"] or raw.stat().st_size != metadata["size"]:
        raise ValueError("Dataset hash or size differs from the DVC pointer")
    tracked = subprocess.check_output(["git", "ls-files", "--", str(raw)], text=True)
    ignored = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", str(raw)], check=False
    )
    if tracked.strip() or ignored.returncode != 0:
        raise ValueError("The raw CSV must be ignored and not tracked by Git")
    return {
        "path": raw.as_posix(),
        "md5": actual,
        "size": raw.stat().st_size,
        "git_tracked": False,
        "git_ignored": True,
        "data_checks": validate_data(load_raw_data(str(raw))),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pointer", default="data/raw/ev_charging_stations.csv.dvc")
    args = parser.parse_args()
    print(json.dumps(verify_dataset(args.pointer), indent=2))
