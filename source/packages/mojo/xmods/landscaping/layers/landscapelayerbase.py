
from typing import TYPE_CHECKING

import weakref

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape

class LandscapeLayerBase:

    def __init__(self, lscape: Landscape):
        self._lscape_ref = weakref.ref(lscape)
        return
    
    @property
    def landscape(self):
        lscape = self._lscape_ref()
        return lscape