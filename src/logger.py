"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import sys
import logging


def get_logger(log_level: int, logger_name: str) -> logging.Logger:
    """create a custom stdout Logger

    :param LoggerLevel: [Required] Level of logger, INFO< DEBUG< WARNING< ERROR< CRITICAL
        CRITICAL = 50
        FATAL = CRITICAL
        ERROR = 40
        WARNING = 30
        WARN = WARNING
        INFO = 20
        DEBUG = 10
        NOTSET = 0
    :type LoggerLevel: int

    :param LoggerName: [Required] name of the logger
    :type LoggerName: str

    :returns:
        a custom logging.Logger object with given specification's

    """
    log_level = log_level or logging.DEBUG
    log_format = logging.Formatter(
        f"[{logger_name}" + "- %(levelname)s] [%(asctime)s] - %(message)s"
    )
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    return logger
