from __future__ import annotations

import importlib
import sys
from pathlib import Path


def _get_policy_checker():
    policy = importlib.import_module("demo.policy")
    for name in (
        "check_launch",
        "validate_launch",
        "is_launch_allowed",
        "authorize_launch",
        "evaluate_launch",
    ):
        checker = getattr(policy, name, None)
        if callable(checker):
            return checker
    raise AssertionError("demo.policy does not expose a known launch-checking function")


def _malicious_config() -> dict[str, object]:
    return {
        "name": "malicious-demo",
        "transport": "stdio",
        "command": sys.executable,
        "args": ["-c", "print('pwned')"],
        "cwd": ".",
    }


def _benign_config() -> dict[str, object]:
    return {
        "name": "benign_stdio_server",
        "transport": "stdio",
        "command": "python",
        "args": ["-m", "demo.benign_server"],
        "cwd": str(Path.cwd()),
    }


def test_policy_rejects_malicious_launch() -> None:
    checker = _get_policy_checker()

    try:
        result = checker(_malicious_config())
    except Exception as exc:
        assert "not allowed" in str(exc).lower() or "not approved" in str(exc).lower()
    else:
        assert result is False


def test_policy_allows_benign_launch() -> None:
    checker = _get_policy_checker()

    result = checker(_benign_config())
    assert result in (True, None)
