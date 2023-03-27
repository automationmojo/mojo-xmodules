"""
.. module:: landscapeintegrationlayer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`LandscapeItegrationLayer` class which is used
               to load initialize the test landscape and integrate with all the available
               landscape resources.

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

from typing import Any, Dict, List, TYPE_CHECKING

from mojo.xmods.exceptions import SemanticError
from mojo.xmods.landscaping.coordinators.coordinatorbase import CoordinatorBase
from mojo.xmods.landscaping.coupling.coordinatorcoupling import CoordinatorCoupling
from mojo.xmods.landscaping.coupling.integrationcoupling import IntegrationCouplingType
from mojo.xmods.landscaping.layers.landscapinglayerbase import LandscapingLayerBase
from mojo.xmods.landscaping.layers.landscapeconfigurationlayer import LandscapeConfigurationLayer
from mojo.xmods.landscaping.friendlyidentifier import FriendlyIdentifier
from mojo.xmods.landscaping.landscapedevice import LandscapeDevice

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape


class LandscapeIntegrationLayer(LandscapingLayerBase):

    def __init__(self, lscape: "Landscape"):
        super().__init__(lscape)
        self._integrated_devices: Dict[str, LandscapeDevice] = None
        self._integrated_power: Dict[str, Any] = None
        self._integrated_serial: Dict[str, Any] = None

        self._requested_integration_couplings: Dict[str, IntegrationCouplingType] = {}

        self._coordinators_for_devices = {}
        self._coordinators_for_power = {}
        self._coordinators_for_serial = {}

        self._power_request_count = 0
        self._serial_request_count = 0
        return
    
    @property
    def coordinators_for_devices(self) -> Dict[str, CoordinatorBase]:
        coord_table = {}

        lscape = self.landscape
        with lscape.begin_locked_landscape_scope() as locked:
            coord_table = self._coordinators_for_devices.copy()

        return coord_table
    
    @property
    def coordinators_for_power(self) -> Dict[str, CoordinatorBase]:
        coord_table = {}

        lscape = self.landscape
        with lscape.begin_locked_landscape_scope() as locked:
            coord_table = self._coordinators_for_power.copy()

        return coord_table
    
    @property
    def coordinators_for_serial(self) -> Dict[str, CoordinatorBase]:
        coord_table = {}

        lscape = self.landscape
        with lscape.begin_locked_landscape_scope() as locked:
            coord_table = self._coordinators_for_serial.copy()

        return coord_table

    @property
    def integrated_devices(self) -> Dict[str, LandscapeDevice]:
        """
            Provides a thread safe copy of the integration device dictionary.
        """
        idevices = {}

        lscape = self.landscape
        with lscape.begin_locked_landscape_scope() as locked:
            idevices = self._integrated_devices.copy()

        return idevices
    
    @property
    def integrated_power(self) -> Dict[str, Any]:
        """
            Provides a thread safe copy of the integration power dictionary.
        """
        ipower = {}

        lscape = self.landscape
        with lscape.begin_locked_landscape_scope() as locked:
            ipower = self._integrated_power.copy()

        return ipower
    
    @property
    def integrated_serial(self) -> Dict[str, Any]:
        """
            Provides a thread safe copy of the integration serial dictionary.
        """
        iserial = {}

        lscape = self.landscape
        with lscape.begin_locked_landscape_scope() as locked:
            iserial = self._integrated_serial.copy()

        return iserial

    @property
    def requested_integration_couplings(self) -> Dict[str, IntegrationCouplingType]:
        """
            Returns a table of the installed integration couplings found.
        """
        return self._requested_integration_couplings

    def initialize_landscape(self) -> Dict[FriendlyIdentifier, LandscapeDevice]:

        lscape = self.landscape

        with lscape.begin_locked_landscape_scope() as locked:

            layer_config = lscape.layer_configuration

            # Initialize the devices so we know what they are, this will create a LandscapeDevice object for each device
            # and register it in the all_devices table where it can be found by the device coordinators for further activation
            devices = self._initialize_landscape_devices(layer_config)

            if self._power_request_count > 0:
                self._initialize_landscape_power(layer_config)

            if self._serial_request_count > 0:
                self._initialize_landscape_serial(layer_config)

        self._integrated_devices = devices.copy()

        return devices

    def register_integration_dependency(self, coupling: IntegrationCouplingType):
        """
            This method should be called from the attach_to_environment methods from individual couplings
            in order to register the base level integrations.  Integrations can be hierarchical so it
            is only necessary to register the root level integration couplings, the descendant couplings can
            be called from the root level couplings.

            :param role: The name of a role to assign for a coupling.
            :param coupling: The coupling to register for the associated role.
        """

        lscape = self.landscape

        with lscape.begin_locked_landscape_scope() as locked:
            integ_key = coupling.get_integration_key()
            self._requested_integration_couplings[integ_key] = coupling

        return

    def topology_overlay(self) -> None:

        return
    
    def _initialize_landscape_devices(self, layer_config: LandscapeConfigurationLayer) -> Dict[FriendlyIdentifier, LandscapeDevice]:

        unrecognized_device_configs = []

        devices: Dict[FriendlyIdentifier: LandscapeDevice] = {}

        requested_coupling_table = self._requested_integration_couplings

        device_configs = layer_config.get_device_configs()

        if len(device_configs) > 0:
            lscape = self.landscape

            for dev_config_info in device_configs:
                dev_type = dev_config_info["deviceType"]
                dev_integ_key = f"devices:deviceType:{dev_type}"

                if dev_integ_key in requested_coupling_table:
                    coord_coupling: CoordinatorCoupling = requested_coupling_table[dev_integ_key]

                    # If we don't have a device coordinator for this type of device yet,
                    # create one.
                    coordinator = None
                    if dev_integ_key in self._coordinators_for_devices:
                        coordinator = self._coordinators_for_devices[dev_integ_key]
                    else:
                        coordinator = coord_coupling.create_coordinator(lscape)
                        self._coordinators_for_devices[dev_integ_key] = coordinator

                    friendly_id, lsdevice = coordinator.create_landscape_device(lscape, dev_config_info)

                    if lsdevice.is_configured_for_power:
                        self._power_request_count += 1

                    if lsdevice.is_configured_for_serial:
                        self._serial_request_count += 1

                    devices[friendly_id.identity] = lsdevice
                else:
                    unrecognized_device_configs.append(dev_config_info)

        return devices


    def _initialize_landscape_power(self, layer_config: LandscapeConfigurationLayer):

        power_configs = layer_config.get_power_configs()

        if len(power_configs) > 0:
            lscape = self.landscape

            for pwr_config_info in power_configs:
                power_type = pwr_config_info["powerType"]
                power_integ_key = f"power:powerType:{power_type}"

        return


    def _initialize_landscape_serial(self, layer_config: LandscapeConfigurationLayer):

        serial_configs = layer_config.get_serial_configs()

        if len(serial_configs) > 0:
            lscape = self.landscape

            for serial_config_info in serial_configs:
                serial_type = serial_config_info["serialType"]
                serial_integ_key = f"serial:serialType:{serial_type}"

        return
