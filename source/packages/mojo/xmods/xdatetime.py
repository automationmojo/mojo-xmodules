"""
.. module:: xdatetime
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains framework time related functions which extend the functionality to
               the python :module:`time` and  :module:`datetime` modules.

.. note:: The modules that are named `xsomething` like this module are prefixed with an `x` character to
          indicate they extend the functionality of a base python module and the `x` is pre-pended to
          prevent module name collisions with python modules.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


import time

from datetime import datetime

DATETIME_FORMAT_FILESYSTEM = "%Y-%m-%dT%H%MS%S.%f"

DATETIME_FORMAT_TIMESTAMP = "%Y-%m-%dT%H:%M:%S.%f"

def current_time_millis() -> float:
    """
        Current system time in milliseconds

        :returns: Time in milliseconds
    """
    now_ms = time.time() * 1000
    return now_ms

def format_datetime_with_fractional(timestamp: datetime, datetime_format=DATETIME_FORMAT_TIMESTAMP) -> str:
    """
        Format the time in seconds as a fractional in seconds.

        :param tsecs: Time in seconds as a float.

        :returns: Formatted time in (seconds).(fractions of seconds)
    """
    dtstr = timestamp.strftime(datetime_format)
    return dtstr

def format_time_with_fractional(tsecs: float, datetime_format=DATETIME_FORMAT_TIMESTAMP) -> str:
    """
        Format the time in seconds as a fractional in seconds.

        :param tsecs: Time in seconds as a float.

        :returns: Formatted time in (seconds).(fractions of seconds)
    """
    timedt = datetime.fromtimestamp(tsecs)
    dtstr = timedt.strftime(datetime_format)
    return dtstr

def parse_datetime(dtstr: str, datetime_format: str=DATETIME_FORMAT_TIMESTAMP) -> datetime:
    """
        Parses a date time from string and includes the microseconds component.

        :param dtstr: The date in the form of a date time string.
        :param datetime_format: The format string to when parsing the datetime string.

        :returns: The datetime from the parsed string.
    """
    dtobj = datetime.strptime(dtstr, datetime_format)
    return dtobj
