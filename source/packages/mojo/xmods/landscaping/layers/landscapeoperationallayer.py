
from typing import TYPE_CHECKING

from mojo.xmods.landscaping.layers.landscapinglayerbase import LandscapingLayerBase

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape


class LandscapeOperationalLayer(LandscapingLayerBase):

    def __init__(self, lscape: "Landscape"):
        super().__init__(lscape)
        return

