"""Simple in-memory pagination helpers."""
from dataclasses import dataclass
from math import ceil
from typing import Generic, TypeVar

from .core import ValidationError

T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    items: list[T]
    page: int
    per_page: int
    total: int
    pages: int

    @classmethod
    def from_items(cls, items, *, page=1, per_page=20):
        """Build a page from a sequence (for large datasets, paginate in SQL)."""
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValidationError("page must be an integer >= 1")
        if isinstance(per_page, bool) or not isinstance(per_page, int) or per_page < 1:
            raise ValidationError("per_page must be an integer >= 1")
        values = list(items)
        total = len(values)
        pages = ceil(total / per_page) if total else 0
        start = (page - 1) * per_page
        return cls(values[start:start + per_page], page, per_page, total, pages)

    def to_dict(self):
        return {
            "items": self.items,
            "page": self.page,
            "per_page": self.per_page,
            "total": self.total,
            "pages": self.pages,
        }
