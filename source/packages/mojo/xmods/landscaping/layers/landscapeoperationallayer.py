
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape


class LandscapeOperationalLayer:

    def __init__(self, lscape: Landscape):
        super().__init__(lscape)
        return

