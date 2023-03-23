
from typing import List, Type

from mojo.xmods.extension.configured import ExtensionPointsFactory

from mojo.xmods.landscaping.coupling.integrationcoupling import IntegrationCoupling
from mojo.xmods.landscaping.extensionpoints import LandscapingExtentionPoints


class LandscapingExtentionPointsFactory(ExtensionPointsFactory, LandscapingExtentionPoints):

    @classmethod
    def get_landscape_type(self) -> Type:
        from mojo.xmods.landscaping.landscape import Landscape
        return Landscape
    
    @classmethod
    def get_integration_coupling_types(self) -> List[Type[IntegrationCoupling]]:
        """
            Used to lookup and return the most relevant list of integration coupling types.
        """
        return []
