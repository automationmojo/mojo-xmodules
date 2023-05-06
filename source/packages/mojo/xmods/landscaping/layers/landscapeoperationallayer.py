
from typing import Dict, TYPE_CHECKING

from mojo.xmods.landscaping.layers.landscapinglayerbase import LandscapingLayerBase
from mojo.xmods.landscaping.landscapedevicecluster import LandscapeDeviceCluster

from mojo.xmods.landscaping.landscapeparameters import (
    LandscapeActivationParams,
    DEFAULT_LANDSCAPE_ACTIVATION_PARAMS,
)

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape


class LandscapeOperationalLayer(LandscapingLayerBase):

    def __init__(self, lscape: "Landscape"):
        super().__init__(lscape)

        self._operational_clusters: Dict[str, LandscapeDeviceCluster] = {}

        return

    def activate_coordinators(self, activation_params: LandscapeActivationParams):
        """
            Activates the coordinators by having them scan for devices in order to enhance the
            devices.
        """
        lscape = self.landscape

        layer_integ = lscape.layer_integration

        coordinators_for_power = layer_integ.coordinators_for_power
        for coord in coordinators_for_power.values():
            coord.activate(activation_params)

        coordinators_for_serial = layer_integ.coordinators_for_serial
        for coord in coordinators_for_serial.values():
            coord.activate(activation_params)

        coordinators_for_devices = layer_integ.coordinators_for_devices
        for coord in coordinators_for_devices.values():
            coord.activate(activation_params)

        return
    
    def establish_connectivity(self, activation_params: LandscapeActivationParams):
        
        lscape = self.landscape

        layer_integ = lscape.layer_integration

        coordinators_for_devices = layer_integ.coordinators_for_devices
        for coord in coordinators_for_devices.values():
            coord.establish_connectivity(activation_params)

        return
    
    def overlay_toplogy(self, activation_params: LandscapeActivationParams):
        return

    def validate_features(self, activation_params: LandscapeActivationParams):

        if activation_params.validate_features:
            pass

        return
    
    def validate_topology(self, activation_params: LandscapeActivationParams):

        if activation_params.validate_topology:
            pass

        return