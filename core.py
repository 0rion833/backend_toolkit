"""Core exceptions and small configuration/JSON helpers."""
from __future__ import annotations

import json
import os
from typing import Callable, TypeVar

T = TypeVar("T")


class AppError(Exception):
    """Base exception for application-level errors."""


class ValidationError(AppError):
    """Raised when input data fails validation."""


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""


class Config:
    """Read typed values from environment variables."""

    @staticmethod
    def get(key: str, default=None, type_cast=str):
        """Return an environment value converted to the requested type."""
        raw = os.getenv(key)
        if raw is None:
            if default is None:
                raise AppError(f"Required configuration is missing: {key}")
            raw = default
        try:
            return type_cast(raw)
        except (TypeError, ValueError) as exc:
            raise AppError(
                f"Configuration value {key!r} has an invalid type or format"
            ) from exc

    @staticmethod
    def get_bool(key: str, default=None) -> bool:
        """Read a boolean from common true/false environment spellings."""
        raw = os.getenv(key)
        if raw is None:
            if default is None:
                raise AppError(f"Required configuration is missing: {key}")
            return default
        value = raw.strip().lower()
        if value in {"1", "true", "yes", "on"}:
            return True
        if value in {"0", "false", "no", "off"}:
            return False
        raise AppError(f"Configuration value {key!r} must be true or false")


def parse_json(text: str):
    """Parse JSON and raise ValidationError for invalid input."""
    if not isinstance(text, str):
        raise ValidationError("JSON input must be a string")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}"
        ) from exc
