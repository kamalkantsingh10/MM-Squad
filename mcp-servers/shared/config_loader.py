"""Shared config loader for all MM MCP servers.

Each server is independent with its own config.yaml and .env.
Provides utilities for loading per-server config, env, and logging.
"""

import logging
import sys
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

_cached_configs: dict[str, dict[str, Any]] = {}


def load_server_env(server_module_dir: Path) -> None:
    """Load .env file from a server's package directory (does not override existing env vars)."""
    env_file = Path(server_module_dir) / ".env"
    load_dotenv(env_file, override=False)


def load_server_config(server_module_dir: Path) -> dict[str, Any]:
    """Load and cache a server's own config.yaml. Resolves <project-root> placeholders."""
    dir_key = str(server_module_dir)
    if dir_key in _cached_configs:
        return _cached_configs[dir_key]

    config_path = Path(server_module_dir) / "config.yaml"
    with open(config_path) as f:
        raw = yaml.safe_load(f) or {}

    root_str = str(_PROJECT_ROOT)
    for key, value in raw.items():
        if isinstance(value, str) and "<project-root>" in value:
            raw[key] = value.replace("<project-root>", root_str)

    _cached_configs[dir_key] = raw
    return raw


def setup_logging(server_name: str, server_module_dir: Path | None = None) -> logging.Logger:
    """Configure dual logging: stderr + log file in the server's own log/ folder."""
    logger = logging.getLogger(server_name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    # stderr handler
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    # file handler — log inside the server's own directory
    if server_module_dir:
        log_dir = Path(server_module_dir) / "log"
    else:
        log_dir = _PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / f"{server_name}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
