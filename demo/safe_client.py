from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

from .config_loader import load_config
from .policy import PolicyViolation, validate_launch_config


def _launch_command(command: str, args: list[str], cwd: Path) -> int:
    executable = sys.executable if command in {"python", "python.exe", "py"} else command
    print(f"[safe] launching approved server: {command!r} {args!r} cwd={str(cwd)!r}", flush=True)
    result = subprocess.run([executable, *args], cwd=str(cwd), shell=False, check=False)
    print(f"[safe] process exited with code {result.returncode}", flush=True)
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Guarded MCP demo client")
    parser.add_argument("--config", required=True, help="Path to JSON config")
    args = parser.parse_args(argv)

    config_path = Path(args.config).resolve()
    print(f"[safe] loading config from {config_path}", flush=True)

    try:
        config: dict[str, Any] = load_config(config_path)
        validated = validate_launch_config(config)
    except PolicyViolation as exc:
        print(f"[safe] policy violation: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[safe] policy violation: invalid config: {exc}", file=sys.stderr)
        return 1

    print(f"[safe] approved config: {validated['name']!r}", flush=True)
    return _launch_command(validated["command"], validated["args"], validated["cwd"])


if __name__ == "__main__":
    raise SystemExit(main())
