"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import logging
import sys


def get_logger(log_level: int, logger_name: str) -> logging.Logger:
    """
    Create and return a custom stdout logger.

    This logger will output logs in the format:
    [<logger_name> - <LEVEL>] [<timestamp>] - <message>

    :param log_level: Logging level (e.g. logging.DEBUG, logging.INFO, etc.)
    :param logger_name: Name of the logger instance.
    :return: Configured logger instance.
    """
    log_level = log_level or logging.DEBUG

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Prevent duplicate handlers if logger is created multiple times
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(name)s - %(levelname)s] [%(asctime)s] - %(message)s"
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
