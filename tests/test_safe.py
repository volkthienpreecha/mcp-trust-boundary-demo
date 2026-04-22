from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _run_client(module: str, config_path: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    return subprocess.run(
        [sys.executable, "-m", module, "--config", str(config_path)],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_safe_client_rejects_malicious_config() -> None:
    artifact_path = REPO_ROOT / "artifacts" / "pwned.txt"
    artifact_path.unlink(missing_ok=True)
    config_path = REPO_ROOT / "configs" / "malicious_demo.json"

    result = _run_client("demo.safe_client", config_path, REPO_ROOT)

    combined_output = (result.stdout + "\n" + result.stderr).lower()
    assert result.returncode != 0
    assert "policy violation:" in combined_output
    assert not artifact_path.exists()


def test_safe_client_accepts_benign_config() -> None:
    artifact_path = REPO_ROOT / "artifacts" / "benign_server_ran.txt"
    artifact_path.unlink(missing_ok=True)
    config_path = REPO_ROOT / "configs" / "benign.json"

    result = _run_client("demo.safe_client", config_path, REPO_ROOT)

    assert result.returncode == 0, result.stderr or result.stdout
    assert artifact_path.exists()
