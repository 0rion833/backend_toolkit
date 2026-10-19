"""A small SQLite context manager built on the standard library."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from .core import AppError


class SQLiteDB:
    """Open a SQLite connection for a context and close it on exit.

    Successful contexts commit; contexts exited with an exception roll back.
    Always pass SQL values through params rather than interpolating strings.
    """

    def __init__(self, path: str | Path = "app.db", *, timeout: float = 5.0):
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.path = str(path)
        self.timeout = timeout
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.path, timeout=self.timeout)
            self.conn.row_factory = sqlite3.Row
            return self
        except sqlite3.Error as exc:
            raise AppError("Could not open SQLite database") from exc

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is None:
            return False
        try:
            if exc_type is not None:
                self.conn.rollback()
            else:
                self.conn.commit()
        finally:
            self.conn.close()
            self.conn = None
        return False

    def _connection(self):
        if self.conn is None:
            raise RuntimeError("SQLiteDB must be used inside a 'with' block")
        return self.conn

    def execute(self, sql: str, params=()):
        """Execute SQL with bound parameters and return a cursor."""
        try:
            return self._connection().execute(sql, params)
        except sqlite3.Error as exc:
            raise AppError("SQLite query failed") from exc

    def executemany(self, sql: str, rows):
        """Execute a parameterized statement for multiple parameter sets."""
        try:
            return self._connection().executemany(sql, rows)
        except sqlite3.Error as exc:
            raise AppError("SQLite batch query failed") from exc

    def fetchone(self, sql: str, params=()):
        """Return one row as a dictionary, or None when no row matches."""
        row = self.execute(sql, params).fetchone()
        return dict(row) if row is not None else None

    def fetchall(self, sql: str, params=()):
        """Return all matching rows as dictionaries."""
        return [dict(row) for row in self.execute(sql, params).fetchall()]
