"""Convert common Python values into JSON-friendly data."""
from __future__ import annotations

import dataclasses
import json
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID


def to_primitive(value: Any):
    """Recursively convert common objects to JSON-compatible primitives."""
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return to_primitive(dataclasses.asdict(value))
    if isinstance(value, dict):
        return {str(key): to_primitive(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_primitive(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, (UUID, Path)):
        return str(value)
    if isinstance(value, Enum):
        return to_primitive(value.value)
    if hasattr(value, "to_dict") and callable(value.to_dict):
        return to_primitive(value.to_dict())
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"Unsupported value for JSON serialization: {type(value).__name__}")


def to_json(value: Any, *, indent=2, ensure_ascii=False) -> str:
    """Serialize supported values to JSON text."""
    return json.dumps(to_primitive(value), indent=indent, ensure_ascii=ensure_ascii)
