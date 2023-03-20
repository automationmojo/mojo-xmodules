
from typing import List, Protocol, Type

from mojo.xmods.xcollections.superfactory import ExtensionPointsFactory

class LandscapingExtentionPoints(Protocol):

    def get_landscape_type(self) -> Type:
        """
            Used to lookup and return the most relevant `Landscape` type.
        """

    def get_integration_coupling_types(self) -> List[Type]:
        """
            Used to lookup and return the most relevant list of integration coupling types.
        """

    
class XModulesExtentionPointsFactory(ExtensionPointsFactory):


    def get_landscape_type(self) -> Type:
        from mojo.xmods.landscaping.landscape import Landscape
        return Landscape
    
    def get_integration_coupling_types(self) -> List[Type]:
        """
            Used to lookup and return the most relevant list of integration coupling types.
        """
        return []