"""
.. module:: xconvert
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains functions for type conversions.

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

from typing import Union

def parse_bool(val: Union[str, bytes]) -> bool:
    """
        Processes the value provided and converts the string to a boolean based
        on common expressions of boolean logic.  True, False, Yes, No, 1, 0
    """

    val = safe_as_str(val).lower()

    rtnval = None

    if val in ["true", "yes", "1"]:
        rtnval = True
    elif val in ["false", "no", "0"]:
        rtnval = False
    else:
        raise ValueError(f"Invalid boolean expression passed to 'parse_bool'. val='{val}'")

    return rtnval

def safe_as_bytes(val: Union[str, bytes]) -> bytes:
    """
        Ensures that the 'val' parameter is a bytes object.

        :param val: A str or bytes value that needs to be converted to bytes.

        :returns: The input value converted to a bytes
    """
    if isinstance(val, str):
        val = val.encode('utf-8')
    return val

def safe_as_str(val: Union[str, bytes]) -> str:
    """
        Ensures that the 'val' parameter is a str object.

        :param val: A str or bytes value that needs to be converted to str.

        :returns: The input value converted to a str
    """
    if isinstance(val, bytes):
        val = val.decode('utf-8')
    return val
