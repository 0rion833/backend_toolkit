"""Dependency-free helpers for small Python backend projects."""

from .core import AppError, Config, NotFoundError, ValidationError, parse_json
from .db import SQLiteDB
from .decorators import delay, retry
from .logging_utils import configure_logging, get_logger
from .models import BaseModel
from .pagination import Page
from .result import Result
from .serialization import to_json, to_primitive
from .validators import (
    check_bool, check_choice, check_int, check_mapping, check_number, check_str,
)

__all__ = [
    "AppError", "BaseModel", "Config", "NotFoundError", "Page", "Result",
    "SQLiteDB", "ValidationError", "check_bool", "check_choice", "check_int",
    "check_mapping", "check_number", "check_str", "configure_logging", "delay",
    "get_logger", "parse_json", "retry", "to_json", "to_primitive",
]
