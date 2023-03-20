
from typing import Dict, List, Type, TYPE_CHECKING

import logging

from mojo.xmods.wellknown.singletons import SuperFactorySinglton

from mojo.xmods.landscaping.coupling.integrationcoupling import IntegrationCouplingType
from mojo.xmods.landscaping.extensionpoints import LandscapingExtentionPoints
from mojo.xmods.landscaping.layers.landscapelayerbase import LandscapeLayerBase

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape

class LandscapeInstallationLayer(LandscapeLayerBase):

    logger = logging.getLogger()

    def __init__(self, lscape: Landscape):
        super().__init__(lscape)

        self._installed_integration_couplings: Dict[str, IntegrationCouplingType]

        self._load_integration_coupling_types()
        return

    @property
    def installed_integration_couplings(self) -> Dict[str, IntegrationCouplingType]:
        """
            Returns a table of the installed integration couplings found.
        """
        return self.installed_integration_couplings

    def _load_integration_coupling_types(self):

        super_factory = SuperFactorySinglton()
        for integration_coupling_types in super_factory.interate_override_types_for_each(
            LandscapingExtentionPoints.get_integration_coupling_types):

            for itype in integration_coupling_types:
                itype: IntegrationCouplingType = itype
                integration_key = f"{itype.integration_section}:{itype.integration_leaf}:{itype.integration_class}"
                self._installed_integration_couplings[integration_key] = itype

        return
