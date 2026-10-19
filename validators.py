"""Small, dependency-free validation helpers."""
from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from typing import TypeVar

from .core import ValidationError

T = TypeVar("T")


def check_int(val, name="value", *, minimum=None, maximum=None) -> int:
    """Validate an integer, excluding bool, with optional bounds."""
    if isinstance(val, bool) or not isinstance(val, int):
        raise ValidationError(f"{name!r} must be an integer")
    if minimum is not None and val < minimum:
        raise ValidationError(f"{name!r} must be at least {minimum}")
    if maximum is not None and val > maximum:
        raise ValidationError(f"{name!r} must be at most {maximum}")
    return val


def check_str(
    val, name="value", *, allow_empty=False, strip=False,
    min_length=None, max_length=None
) -> str:
    """Validate a string and optionally normalize surrounding whitespace."""
    if not isinstance(val, str):
        raise ValidationError(f"{name!r} must be a string")
    result = val.strip() if strip else val
    if not allow_empty and not result.strip():
        raise ValidationError(f"{name!r} must not be empty")
    if min_length is not None and len(result) < min_length:
        raise ValidationError(f"{name!r} must contain at least {min_length} characters")
    if max_length is not None and len(result) > max_length:
        raise ValidationError(f"{name!r} must contain at most {max_length} characters")
    return result


def check_bool(val, name="value") -> bool:
    """Validate a boolean without accepting integers 0 and 1."""
    if not isinstance(val, bool):
        raise ValidationError(f"{name!r} must be a boolean")
    return val


def check_number(val, name="value", *, minimum=None, maximum=None):
    """Validate a finite int/float, excluding bool, with optional bounds."""
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise ValidationError(f"{name!r} must be a number")
    if not math.isfinite(val):
        raise ValidationError(f"{name!r} must be finite")
    if minimum is not None and val < minimum:
        raise ValidationError(f"{name!r} must be at least {minimum}")
    if maximum is not None and val > maximum:
        raise ValidationError(f"{name!r} must be at most {maximum}")
    return val


def check_choice(val: T, choices: Iterable[T], name="value") -> T:
    """Ensure a value belongs to an allowed collection."""
    allowed = tuple(choices)
    if val not in allowed:
        raise ValidationError(f"{name!r} must be one of: {allowed!r}")
    return val


def check_mapping(val, name="value") -> Mapping:
    """Validate that a value is a mapping."""
    if not isinstance(val, Mapping):
        raise ValidationError(f"{name!r} must be a mapping")
    return val
