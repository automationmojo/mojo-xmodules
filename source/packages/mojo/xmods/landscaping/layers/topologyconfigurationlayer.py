
from typing import TYPE_CHECKING

import logging
import weakref

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape

class TopologyConfigurationLayer:

    logger = logging.getLogger()

    def __init__(self, lscape: "Landscape"):
        self._lscape_ref = weakref.ref(lscape)
        return

    @property
    def landscape(self):
        return self._lscape_ref()
