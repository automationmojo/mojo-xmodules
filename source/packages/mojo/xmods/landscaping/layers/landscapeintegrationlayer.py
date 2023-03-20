
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape


class LandscapeIntegrationLayer:

    def __init__(self, lscape: Landscape):
        super().__init__(lscape)
        return
    
    def topology_overlay(self) -> None:
        return
