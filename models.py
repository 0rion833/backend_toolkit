"""A lightweight annotation-based model for small projects."""
from __future__ import annotations

from typing import get_type_hints

from .core import ValidationError


class BaseModel:
    """Minimal model with required annotated fields and strict basic types.

    Subclasses declare fields using annotations and can define class defaults.
    This is intentionally small; it is not a replacement for a schema library.
    """

    def __init__(self, **kwargs):
        hints = {}
        for cls in reversed(type(self).__mro__):
            if cls is BaseModel:
                continue
            try:
                hints.update(get_type_hints(cls))
            except (NameError, TypeError):
                hints.update(getattr(cls, "__annotations__", {}))

        unknown = set(kwargs) - set(hints)
        if unknown:
            raise ValidationError(f"Unknown fields: {', '.join(sorted(unknown))}")

        for name, expected_type in hints.items():
            if name in kwargs:
                value = kwargs[name]
            elif hasattr(type(self), name):
                value = getattr(type(self), name)
            else:
                raise ValidationError(f"Missing required field: {name}")

            if expected_type is int:
                if isinstance(value, bool) or not isinstance(value, int):
                    raise ValidationError(f"{name!r} must be an integer")
            elif expected_type is str:
                if not isinstance(value, str):
                    raise ValidationError(f"{name!r} must be a string")
            elif expected_type is bool:
                if not isinstance(value, bool):
                    raise ValidationError(f"{name!r} must be a boolean")
            elif isinstance(expected_type, type) and not isinstance(value, expected_type):
                raise ValidationError(f"{name!r} must be {expected_type.__name__}")

            setattr(self, name, value)

    def to_dict(self) -> dict:
        """Return the model's declared fields as a dictionary."""
        fields = {}
        for cls in reversed(type(self).__mro__):
            if cls is BaseModel:
                continue
            fields.update(getattr(cls, "__annotations__", {}))
        return {name: getattr(self, name) for name in fields}

    def __repr__(self) -> str:
        values = ", ".join(f"{name}={value!r}" for name, value in self.to_dict().items())
        return f"{type(self).__name__}({values})"
