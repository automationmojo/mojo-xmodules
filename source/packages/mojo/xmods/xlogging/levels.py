"""
.. module:: levels
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the logging level declarations.
.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import logging

from enum import IntEnum


class LogLevel(IntEnum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    QUIET = 1000


logging.addLevelName(LogLevel.QUIET.value, "QUIET")

LOG_LEVEL_NAMES = [member.name for member in LogLevel]
