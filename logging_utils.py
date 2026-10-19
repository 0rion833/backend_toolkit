"""Small logging configuration helpers."""
import logging
import sys


def configure_logging(level=logging.INFO, *, fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"):
    """Configure basic console logging; call once near application startup."""
    logging.basicConfig(
        level=level,
        format=fmt,
        stream=sys.stdout,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger."""
    return logging.getLogger(name)
