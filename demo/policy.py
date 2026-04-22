from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .config_loader import repo_root


class PolicyViolation(ValueError):
    pass


APPROVED_SERVERS: dict[str, dict[str, Any]] = {
    "benign_stdio_server": {
        "transport": "stdio",
        "command": "python",
        "args": ["-m", "demo.benign_server"],
    }
}


def _require_str(config: Mapping[str, Any], key: str) -> str:
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PolicyViolation(f"field {key!r} must be a non-empty string")
    return value.strip()


def _require_args(config: Mapping[str, Any]) -> list[str]:
    value = config.get("args")
    if not isinstance(value, list):
        raise PolicyViolation("field 'args' must be a list")
    args = [str(item) for item in value]
    if any(arg == "-c" for arg in args):
        raise PolicyViolation("inline execution via '-c' is not allowed")
    return args


def validate_launch_config(config: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(config, Mapping):
        raise PolicyViolation("config must be a JSON object")

    name = _require_str(config, "name")
    transport = _require_str(config, "transport")
    command = _require_str(config, "command")
    args = _require_args(config)

    approved = APPROVED_SERVERS.get(name)
    if approved is None:
        raise PolicyViolation(f"server name {name!r} is not approved")

    if transport != approved["transport"]:
        raise PolicyViolation(
            f"transport {transport!r} is not approved for server {name!r}"
        )

    if command != approved["command"]:
        raise PolicyViolation(f"command {command!r} is not on the approved registry")

    if args != approved["args"]:
        raise PolicyViolation(
            f"args {args!r} do not match the approved registry entry for {name!r}"
        )

    cwd_value = config.get("cwd")
    if not isinstance(cwd_value, str) or not cwd_value.strip():
        raise PolicyViolation("field 'cwd' must be a non-empty string")

    cwd = Path(cwd_value).resolve()
    root = repo_root().resolve()
    if cwd != root:
        raise PolicyViolation("cwd must resolve to the repository root")

    return {
        "name": name,
        "transport": transport,
        "command": command,
        "args": args,
        "cwd": cwd,
    }


def check_launch(config: Mapping[str, Any]) -> bool:
    validate_launch_config(config)
    return True
