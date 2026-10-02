"""Import your OAuth client JSON into ignored local DVC configuration."""

import argparse
import json
from pathlib import Path

from dvc.config import Config


def configure_drive(client_json):
    document = json.loads(Path(client_json).read_text(encoding="utf-8"))
    client = document.get("installed") or document.get("web")
    if not client or not all(client.get(key) for key in ["client_id", "client_secret"]):
        raise ValueError(
            "Expected a Google OAuth client JSON with client_id and client_secret"
        )
    config = Config(".dvc")
    if (
        not config.get("remote", {})
        .get("storage", {})
        .get("url", "")
        .startswith("gdrive://")
    ):
        raise ValueError(
            "The repository must already have Faheem's storage Drive remote"
        )
    with config.edit(level="local") as local:
        remote = local.setdefault("remote", {}).setdefault("storage", {})
        remote["gdrive_client_id"] = client["client_id"]
        remote["gdrive_client_secret"] = client["client_secret"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "client_json", help="Local path; keep this file outside the repository"
    )
    args = parser.parse_args()
    configure_drive(args.client_json)
    print("OAuth client configured in .dvc/config.local; credentials were not printed.")
    print("Run uv run dvc pull and authorize using your own Google account.")
