from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
from typing import Any


def _load_config(path: Path) -> dict[str, Any]:
    try:
        from .config_loader import load_config  # type: ignore
    except ImportError:
        load_config = None

    if load_config is not None:
        return load_config(path)

    import json

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Unsafe MCP demo client")
    parser.add_argument("--config", required=True, help="Path to JSON config")
    args = parser.parse_args(argv)

    config_path = Path(args.config).resolve()
    config = _load_config(config_path)

    print(f"[unsafe] loaded config: {config.get('name')!r}", flush=True)

    command = config["command"]
    command_args = list(config.get("args", []))
    cwd = Path(config.get("cwd", ".")).resolve()

    print(f"[unsafe] launching: {command!r} {command_args!r} cwd={str(cwd)!r}", flush=True)
    result = subprocess.run([command, *command_args], cwd=str(cwd), shell=False, check=False)
    print(f"[unsafe] process exited with code {result.returncode}", flush=True)

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
