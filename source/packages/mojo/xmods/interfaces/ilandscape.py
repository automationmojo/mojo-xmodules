"""
.. module:: ilandscape
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains a protocol for interoperating with compute
               environment shared resources.

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

from typing import Any, List, Protocol, TYPE_CHECKING

from mojo.xmods.interfaces.iincludefilter import IIncludeFilter
from mojo.xmods.interfaces.iexcludefilter import IExcludeFilter
from mojo.xmods.interfaces.ilandscapedevice import ILandscapeDevice

class ILandscape(Protocol):
    """
        The ILandscape interface is used to provide a common interface working with
        compute environment shared resources.
    """

    @property
    def credentials(self) -> dict:
        """
            Returns a dictionary of named credentials.
        """

    @property
    def environment(self) -> dict:
        """
            Returns the environment section of the landscape configuration.
        """
    
    @property
    def name(self) -> str:
        """
            Returns the name associated with the landscape.
        """
    
    @property
    def runtime_configuration(self) -> dict:
        """
            Returns the configuration dictionary associated with the global runtime context.
        """
    
    def checkin_device(self, device: ILandscapeDevice):
        """
            Returns a landscape device to the the available device pool.
        """

    def checkin_multiple_devices(self, devices: List[ILandscapeDevice]):
        """
            Returns a landscape device to the the available device pool.
        """

    def checkout_device(self, device: ILandscapeDevice):
        """
            Checks out the specified device from the device pool.
        """

    def checkout_devices_with_filters(self, includes: List[IIncludeFilter], 
                                      excludes: List[IExcludeFilter]) -> List[ILandscapeDevice]:
        """
            Checks out a collection of devices using filters to include and exclude devices.
        """

    def checkout_multiple_devices(self, device_list: List[ILandscapeDevice]):
        """
            Checks out the list of specified devices from the device pool.
        """

    def diagnostic(self, diaglabel: str, diags: dict):
        """
            Can be called in order to perform a diagnostic capture across the test landscape.

            :param diaglabel: The label to use for the diagnostic.
            :param diags: A dictionary of diagnostics to run.
        """

    def get_device_configs(self) -> List[dict]:
        """
            Returns the list of device configurations from the landscape.  This will
            skip any device that has a "skip": true member.
        """
    
    def get_devices(self) -> List[ILandscapeDevice]:
        """
            Returns the list of devices from the landscape.  This will skip any device that
            has a "skip": true member.
        """

    def get_devices_with_filters(self, includes: List[IIncludeFilter], 
                                 excludes: List[IExcludeFilter]) -> List[ILandscapeDevice]:
        """
            Returns the list of devices from the landscape while filtering devices by include
            and exclude filters.  This will skip any device that has a "skip": true member.
        """
