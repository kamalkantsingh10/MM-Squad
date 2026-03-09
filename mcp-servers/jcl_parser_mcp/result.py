"""Structured result helpers for MCP tool responses."""

from typing import Any


def make_result(
    data: Any = None,
    flags: list[dict] | None = None,
    message: str = "",
    status: str = "ok",
) -> dict:
    return {
        "status": status,
        "data": data,
        "flags": flags if flags is not None else [],
        "message": message,
    }


def make_error(message: str, flags: list[dict] | None = None) -> dict:
    return make_result(status="error", message=message, flags=flags)


def make_warning(data: Any, message: str, flags: list[dict] | None = None) -> dict:
    return make_result(status="warning", data=data, message=message, flags=flags)
