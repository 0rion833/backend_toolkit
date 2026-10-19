"""A tiny result container for API/service return values."""
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    ok: bool
    data: T | None = None
    error: str | None = None

    @classmethod
    def success(cls, data=None):
        return cls(ok=True, data=data)

    @classmethod
    def failure(cls, error: str):
        if not error:
            raise ValueError("error must not be empty")
        return cls(ok=False, error=error)

    def to_dict(self):
        return {"ok": self.ok, "data": self.data, "error": self.error}
