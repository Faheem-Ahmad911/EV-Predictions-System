"""Exercise DVC discovery, caching and parameter invalidation without Drive."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

from src.smoke import sample_data


def test_dvc_graph_reproduces_and_invalidates_only_changed_stages(tmp_path):
    root = Path(__file__).resolve().parents[1]
    for name in ["dvc.yaml", "uv.lock", ".python-version", ".gitignore"]:
        shutil.copyfile(root / name, tmp_path / name)
    shutil.copytree(
        root / "src", tmp_path / "src", ignore=shutil.ignore_patterns("__pycache__")
    )
    (tmp_path / "configs").mkdir()
    (tmp_path / "data/raw").mkdir(parents=True)
    shutil.copyfile(root / "data/.gitignore", tmp_path / "data/.gitignore")
    params = yaml.safe_load((root / "configs/params.yaml").read_text())
    params["train"]["n_estimators"] = 5
    config = tmp_path / "configs/params.yaml"
    config.write_text(yaml.safe_dump(params), encoding="utf-8")
    sample_data(50).to_csv(tmp_path / params["data"]["raw_path"], index=False)
    env = {
        **os.environ,
        "PATH": str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"],
    }

    def run(*args):
        result = subprocess.run(
            args,
            cwd=tmp_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        return result.stdout

    run("git", "init")
    run(sys.executable, "-m", "dvc", "init")
    run(sys.executable, "-m", "dvc", "add", params["data"]["raw_path"])
    # An untargeted command must find the nested pointer, including on Windows.
    dag = run(sys.executable, "-m", "dvc", "dag", "--dot")
    assert "ev_charging_stations.csv.dvc" in dag
    run(sys.executable, "-m", "dvc", "repro")
    metrics_file = tmp_path / "metrics.json"
    first_metrics = json.loads(metrics_file.read_text())
    first_lock = yaml.safe_load((tmp_path / "dvc.lock").read_text())
    assert first_metrics["n_test_samples"] == 10
    assert "didn't change" in run(sys.executable, "-m", "dvc", "repro")
    assert json.loads(metrics_file.read_text()) == first_metrics
    params["train"]["n_estimators"] = 7
    config.write_text(yaml.safe_dump(params), encoding="utf-8")
    run(sys.executable, "-m", "dvc", "repro")
    second_lock = yaml.safe_load((tmp_path / "dvc.lock").read_text())
    assert first_lock["stages"]["prepare"] == second_lock["stages"]["prepare"]
    assert first_lock["stages"]["train"] != second_lock["stages"]["train"]
    assert json.loads(metrics_file.read_text())["n_estimators"] == 7
