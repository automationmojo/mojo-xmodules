
"""
.. module:: enumerations
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing enumerations used by eventing modules.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


from enum import IntEnum

class EventedVariableState(IntEnum):
    """
        An enumeration that indicates the state of the event variable.
    """
    UnInitialized = 0
    Default = 1
    Valid = 2
    Stale = 3
