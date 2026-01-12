"""
Logger Utility

Centralized logging configuration for OCR pipeline.

Author: Jason Cruz
Institution: Universidad del Pacífico - CIUP
Date: January 2026
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    log_file: Optional[str] = "OCR/logs/ocr_pipeline.log",
    level: str = "INFO",
    format_string: Optional[str] = None,
    console_output: bool = True
) -> None:
    """
    Configure logging for OCR pipeline.

    Args:
        log_file: Path to log file (None = no file logging)
        level: Logging level ("DEBUG", "INFO", "WARNING", "ERROR")
        format_string: Custom format string (None = use default)
        console_output: Enable console logging
    """
    # Convert level string to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Default format
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(numeric_level)

    # Remove existing handlers
    logger.handlers.clear()

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(logging.Formatter(format_string))
        logger.addHandler(file_handler)

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)

        # Simpler format for console
        console_format = "%(levelname)s: %(message)s"
        if level.upper() == "DEBUG":
            console_format = "%(name)s - %(levelname)s: %(message)s"

        console_handler.setFormatter(logging.Formatter(console_format))
        logger.addHandler(console_handler)

    logging.info(f"Logging initialized: level={level}, file={log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance for a module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


if __name__ == "__main__":
    # Test logger
    setup_logging(
        log_file="OCR/logs/test.log",
        level="DEBUG",
        console_output=True
    )

    logger = get_logger(__name__)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    print("\n✓ Logging test complete. Check OCR/logs/test.log")
