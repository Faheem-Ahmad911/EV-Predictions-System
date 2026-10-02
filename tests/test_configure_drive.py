"""OAuth setup must preserve the shared remote and write only local config."""

import json
import subprocess
from pathlib import Path

from dvc.config import Config

from src.configure_drive import configure_drive


def test_oauth_client_is_saved_only_to_ignored_local_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], check=True, capture_output=True)
    Path(".dvc").mkdir()
    shared = Path(".dvc/config")
    shared.write_text(
        '[core]\n    remote = storage\n[remote "storage"]\n    url = gdrive://shared-folder\n'
    )
    Path(".gitignore").write_text(".dvc/config.local\n")
    original = shared.read_bytes()
    client_json = Path("client.json")
    client_json.write_text(
        json.dumps(
            {
                "installed": {
                    "client_id": "test.apps.googleusercontent.com",
                    "client_secret": "test-only-placeholder",  # pragma: allowlist secret
                }
            }
        )
    )
    configure_drive(client_json)
    assert shared.read_bytes() == original
    config = Config(".dvc")
    assert (
        config["remote"]["storage"]["gdrive_client_id"]
        == "test.apps.googleusercontent.com"
    )
    assert (
        config["remote"]["storage"]["gdrive_client_secret"]
        == json.loads(client_json.read_text())["installed"]["client_secret"]
    )
    assert (
        subprocess.run(
            ["git", "check-ignore", "--quiet", ".dvc/config.local"], check=False
        ).returncode
        == 0
    )
