"""
.. module:: includefilters
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing various device include filters.

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

from typing import Any

from mojo.xmods.interfaces.iincludefilter import IIncludeFilter

from mojo.xmods.landscaping.landscapedevice import LandscapeDevice


class IncludeDeviceByGroup(IIncludeFilter):

    def __init__(self, group: str) -> None:
        super().__init__()
        self._group = group
        return

    def should_include(self, check_object: Any) -> bool:
        """
            Determines if a device matches an include criteria internalized in the filter object.

            :param check_object: The object to check for a match with the exclude criteria.
        """
        include = False

        if isinstance(check_object, LandscapeDevice):
            lsdevice: LandscapeDevice = check_object
            if lsdevice.group == self._group:
                include = True

        return include


class IncludeDeviceByName(IIncludeFilter):

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name
        return

    def should_include(self, check_object: Any) -> bool:
        """
            Determines if a device matches an include criteria internalized in the filter object.

            :param check_object: The object to check for a match with the exclude criteria.
        """
        include = False

        if isinstance(check_object, LandscapeDevice):
            lsdevice: LandscapeDevice = check_object
            if lsdevice.name == self._name:
                include = True

        return include


class IncludeDeviceByDeviceType(IIncludeFilter):

    def __init__(self, device_type: str) -> None:
        super().__init__()
        self._device_type = device_type
        return

    def should_include(self, check_object: Any) -> bool:
        """
            Determines if a device matches an include criteria internalized in the filter object.

            :param check_object: The object to check for a match with the exclude criteria.
        """
        include = False

        if isinstance(check_object, LandscapeDevice):
            lsdevice: LandscapeDevice = check_object
            if lsdevice.device_type == self._device_type:
                include = True

        return include
