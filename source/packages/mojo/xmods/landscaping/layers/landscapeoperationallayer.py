
from typing import Dict, TYPE_CHECKING

from mojo.xmods.landscaping.layers.landscapinglayerbase import LandscapingLayerBase
from mojo.xmods.landscaping.layers.landscapeintegrationlayer import LandscapeIntegrationLayer
from mojo.xmods.landscaping.landscapedevicecluster import LandscapeDeviceCluster
from mojo.xmods.landscaping.cluster.nodecoordinatorbase import NodeCoordinatorBase

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

    @property
    def operational_clusters(self) -> Dict[str, LandscapeDeviceCluster]:
        cluster_table = {}

        lscape = self.landscape
        with lscape.begin_locked_landscape_scope() as locked:
            cluster_table = self._operational_clusters.copy()
        
        return cluster_table

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

        lscape = self.landscape

        topology_info = lscape.layer_configuration.topology_info
        integ_layer = lscape.layer_integration

        self._create_clusters(integ_layer, topology_info)

        return

    def validate_features(self, activation_params: LandscapeActivationParams):

        if activation_params.validate_features:
            pass

        return
    
    def validate_topology(self, activation_params: LandscapeActivationParams):

        if activation_params.validate_topology:
            pass

        return

    def _create_clusters(self, integ_layer: LandscapeIntegrationLayer, topology_info: Dict[str, Any]):

        table_of_device_groups = integ_layer.integrated_device_groups

        # ================= EXAMPLE ===================
        #
        #   - name: primary
        #     group: cluster/primary
        #     nodes:
        #         - mwalker-smbtest-green
        #         - mwalker-smbtest-orange
        #         - mwalker-smbtest-red
        #     spares:
        #         - mwalker-smbtest-yellow

        if "clusters" in topology_info:
            clusters = topology_info["clusters"]
            for cinfo in clusters:
                cname = cinfo["name"]
                group_name = cinfo["group"]

                nodes = []
                if "nodes" in topology_info:
                    nodes = topology_info["nodes"]
                
                spares = []
                if "spares" in topology_info:
                    spares = topology_info["spares"]

                if group_name in table_of_device_groups:
                    cgroup = table_of_device_groups[group_name]

                    coordinator: NodeCoordinatorBase = cgroup.coordinator
                    cluster = coordinator.create_cluster_for_devices(cname, cgroup, nodes, spares)

                    self._operational_clusters[cname] = cluster
        
        return