"""Logging configuration for the application runtime.

This module deliberately contains no domain or workflow behavior. The composition
root can call ``configure_logging`` before application components are constructed.
"""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(log_directory: Path, level: str = "INFO") -> None:
    """Configure a console logger and a local UTF-8 application log file.

    The caller owns configuration values and chooses when startup occurs. Existing
    handlers are left unchanged so importing this project has no side effects.
    """
    log_directory.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("automation")
    logger.setLevel(level.upper())
    logger.propagate = False

    if logger.handlers:
        return

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_directory / "automation.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

