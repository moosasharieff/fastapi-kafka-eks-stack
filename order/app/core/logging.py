"""Logger setup utility for configuring application-wide logging behavior."""

import logging


def init_logger() -> None:
    """
    Initialize the root logger with a consistent format and INFO log level.

    This sets the basic configuration for logging across the application,
    including timestamp, log level, logger name, and the message.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
