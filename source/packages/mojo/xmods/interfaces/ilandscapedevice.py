"""
.. module:: ilandscapedevice
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains protocol for a Landscape device

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

from typing import Any, List, Protocol

class ILandscapeDevice(Protocol):
    """
        The ILandscapeDevice interface is used to provide a common interface for performing
        basic interop with a landscape device.
    """
