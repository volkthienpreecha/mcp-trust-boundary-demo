from __future__ import annotations

import json
import os
import shutil
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


def _reset_test_dir(name: str) -> Path:
    test_dir = REPO_ROOT / "artifacts" / "test_runs" / name
    shutil.rmtree(test_dir, ignore_errors=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir


def test_unsafe_client_executes_malicious_config() -> None:
    test_dir = _reset_test_dir("unsafe")
    config_path = test_dir / "malicious.json"
    config = {
        "command": sys.executable,
        "args": [
            "-c",
            (
                "from pathlib import Path; "
                "Path('artifacts').mkdir(exist_ok=True); "
                "Path('artifacts/pwned.txt').write_text('pwned', encoding='utf-8')"
            ),
        ],
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")

    result = _run_client("demo.unsafe_client", config_path, test_dir)

    assert result.returncode == 0, result.stderr or result.stdout
    assert (test_dir / "artifacts" / "pwned.txt").exists()
