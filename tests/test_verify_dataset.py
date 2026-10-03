"""Prevent a substituted or Git-tracked CSV from passing teammate verification."""

import hashlib
import subprocess

import pytest
import yaml

from src.smoke import sample_data
from src.verify_dataset import verify_dataset


@pytest.fixture
def dataset_checkout(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], check=True, capture_output=True)
    (tmp_path / ".gitignore").write_text("*.csv\n")
    raw = tmp_path / "stations.csv"
    sample_data(10).to_csv(raw, index=False)
    pointer = tmp_path / "stations.csv.dvc"
    pointer.write_text(
        yaml.safe_dump(
            {
                "outs": [
                    {
                        "path": raw.name,
                        "md5": hashlib.md5(raw.read_bytes()).hexdigest(),
                        "size": raw.stat().st_size,
                        "hash": "md5",
                    }
                ]
            }
        )
    )
    return pointer, raw


def test_verified_file_is_ignored_and_matches_pointer(dataset_checkout):
    pointer, _ = dataset_checkout
    result = verify_dataset(pointer)
    assert result["git_ignored"] and not result["git_tracked"]
    assert result["data_checks"]["rows"] == 10


def test_rejects_substitute_dataset(dataset_checkout):
    pointer, raw = dataset_checkout
    raw.write_bytes(raw.read_bytes().replace(b"Operational", b"Not running"))
    with pytest.raises(ValueError, match="hash or size"):
        verify_dataset(pointer)


def test_rejects_tracked_dataset(dataset_checkout):
    pointer, raw = dataset_checkout
    subprocess.run(["git", "add", "--force", raw.name], check=True)
    with pytest.raises(ValueError, match="ignored and not tracked"):
        verify_dataset(pointer)


def test_missing_dataset_explains_pull(dataset_checkout):
    pointer, raw = dataset_checkout
    raw.unlink()
    with pytest.raises(FileNotFoundError, match="dvc pull"):
        verify_dataset(pointer)
