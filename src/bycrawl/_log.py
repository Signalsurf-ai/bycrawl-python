"""
ByCrawl Logging

Uses loguru. Disabled by default — call enable_logging() to activate.
"""

from __future__ import annotations

from loguru import logger

# Disable by default; users opt-in via bycrawl.enable_logging()
logger.disable("bycrawl")


def enable_logging(level: str = "DEBUG") -> None:
    """Enable SDK logging at the given level."""
    logger.enable("bycrawl")
