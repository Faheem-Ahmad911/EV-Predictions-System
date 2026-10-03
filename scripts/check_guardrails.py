"""Prove that real commits with a large file or fake secret are rejected."""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def verify_guardrails():
    source = Path(__file__).resolve().parents[1]
    env = {
        **os.environ,
        "PATH": str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"],
    }
    with TemporaryDirectory(prefix="ev-guardrail-probe-") as directory:
        root = Path(directory)

        def run(*args, check=True):
            return subprocess.run(
                args,
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                timeout=180,
                check=check,
            )

        run("git", "init")
        for name in [".pre-commit-config.yaml", ".secrets.baseline"]:
            shutil.copyfile(source / name, root / name)
        run(sys.executable, "-m", "pre_commit", "install")
        probes = [
            ("large.bin", b"0" * (5 * 1024 * 1024 - 1) + b"\n", "exceeds 1024 KB"),
            (
                "fake-private-key.txt",
                (
                    b"-----BEGIN PRIVATE KEY-----\n"  # pragma: allowlist secret
                    b"INTENTIONALLY_INVALID_TEST_FIXTURE\n"
                    b"-----END PRIVATE KEY-----\n"
                ),
                "Secret Type: Private Key",
            ),
        ]
        for name, payload, expected in probes:
            (root / name).write_bytes(payload)
            run("git", "add", "--", name)
            result = run(
                "git",
                "-c",
                "user.name=Guardrail fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "-m",
                "test: intentionally rejected fixture",
                check=False,
            )
            output = result.stdout + result.stderr
            print(f"\nCommit probe: {name}\n{output}", flush=True)
            if result.returncode == 0 or expected not in output:
                raise RuntimeError(
                    f"Expected guardrail rejection was not observed for {name}"
                )
            if run("git", "rev-parse", "--verify", "HEAD", check=False).returncode == 0:
                raise RuntimeError("A fixture commit unexpectedly reached history")
            run("git", "rm", "--cached", "--force", "--", name)
            (root / name).unlink()
        print(
            "Both actual commit attempts were rejected. No fixture commit was created."
        )


if __name__ == "__main__":
    verify_guardrails()
