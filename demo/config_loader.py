from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


def repo_root() -> Path:
    return REPO_ROOT


def load_config(config_path: str | Path) -> dict[str, Any]:
    config_file = Path(config_path).resolve()
    data = json.loads(config_file.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("config must be a JSON object")

    args = data.get("args", [])
    if not isinstance(args, list):
        raise ValueError("config field 'args' must be a list")

    normalized = dict(data)
    normalized["config_path"] = str(config_file)
    normalized["config_dir"] = str(config_file.parent)
    normalized["command"] = str(data.get("command", ""))
    normalized["args"] = [str(arg) for arg in args]

    return normalized
