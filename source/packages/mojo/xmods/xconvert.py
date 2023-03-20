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


def safe_as_bytes(val: Union[str, bytes]) -> bytes:
    """
        Ensures that the 'val' parameter is a bytes object.

        :param val: A str or bytes value that needs to be converted to bytes.
        :param val: str or bytes

        :returns: The input value converted to a bytes
    """
    if isinstance(val, str):
        val = val.encode('utf-8')
    return val

def safe_as_str(val: Union[str, bytes]) -> str:
    """
        Ensures that the 'val' parameter is a str object.

        :param val: A str or bytes value that needs to be converted to str.
        :param val: str or bytes

        :returns: The input value converted to a str
    """
    if isinstance(val, bytes):
        val = val.decode('utf-8')
    return val
