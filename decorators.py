"""Reusable decorators for delays and bounded retries."""
from __future__ import annotations

import asyncio
import functools
import inspect
import time


def delay(seconds: float):
    """Wait before calling an async function."""
    if seconds < 0:
        raise ValueError("seconds must be non-negative")

    def decorator(fn):
        if not inspect.iscoroutinefunction(fn):
            raise TypeError("@delay can only decorate async functions")

        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(seconds)
            return await fn(*args, **kwargs)
        return wrapper
    return decorator


def retry(tries=3, delay_sec=1.0, *, exceptions=(Exception,)):
    """Retry sync or async calls a bounded number of times.

    Pass a narrow exception tuple where possible. Avoid retrying operations that
    can cause duplicate side effects unless those operations are idempotent.
    """
    if isinstance(tries, bool) or not isinstance(tries, int) or tries < 1:
        raise ValueError("tries must be an integer >= 1")
    if delay_sec < 0:
        raise ValueError("delay_sec must be non-negative")
    if not exceptions or not all(
        isinstance(item, type) and issubclass(item, Exception)
        for item in exceptions
    ):
        raise TypeError("exceptions must be a non-empty tuple of Exception types")

    def decorator(fn):
        if inspect.iscoroutinefunction(fn):
            @functools.wraps(fn)
            async def async_wrapper(*args, **kwargs):
                for attempt in range(tries):
                    try:
                        return await fn(*args, **kwargs)
                    except exceptions:
                        if attempt == tries - 1:
                            raise
                        await asyncio.sleep(delay_sec)
            return async_wrapper

        @functools.wraps(fn)
        def sync_wrapper(*args, **kwargs):
            for attempt in range(tries):
                try:
                    return fn(*args, **kwargs)
                except exceptions:
                    if attempt == tries - 1:
                        raise
                    time.sleep(delay_sec)
            raise RuntimeError("unreachable")
        return sync_wrapper
    return decorator
