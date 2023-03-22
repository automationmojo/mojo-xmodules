
from typing import TYPE_CHECKING

import logging

from mojo.xmods.landscaping.layers.landscapelayerbase import LandscapeLayerBase

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape

class LandscapeIntegrationLayer(LandscapeLayerBase):

    logger = logging.getLogger()

    def __init__(self, lscape: "Landscape"):
        super().__init__(lscape)
        return
    
    def topology_overlay(self) -> None:
        return
