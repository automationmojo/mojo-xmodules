
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import TYPE_CHECKING

from threading import RLock

from mojo.xmods.xcollections.superfactory import SuperFactory

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape


SUPER_FACTORY_SINGLETON = None
LANDSCAPE_SINGLETON = None


SINGLETON_LOCK = RLock()

def SuperFactorySinglton() -> SuperFactory:
    global SINGLETON_LOCK
    global SUPER_FACTORY_SINGLETON

    # If the singleton is already set, don't bother grabbing a lock
    # to set it.  The full path of the setting of the singleton will only
    # ever be taken once
    if SUPER_FACTORY_SINGLETON is None:
        SINGLETON_LOCK.acquire()
        try:
            if SUPER_FACTORY_SINGLETON is None:
                SUPER_FACTORY_SINGLETON = SuperFactory()
        finally:
            SINGLETON_LOCK.release()

    return SUPER_FACTORY_SINGLETON


def LandscapeSingleton() -> "Landscape":

    global SINGLETON_LOCK
    global LANDSCAPE_SINGLETON

    # If the singleton is already set, don't bother grabbing a lock
    # to set it.  The full path of the setting of the singleton will only
    # ever be taken once
    if LANDSCAPE_SINGLETON is None:
        super_factory = SuperFactorySinglton()

        SINGLETON_LOCK.acquire()
        try:
            from mojo.xmods.extensionpoints import LandscapingExtentionPoints

            if LANDSCAPE_SINGLETON is None:
                LandscapeType = super_factory.get_override_types_by_order(
                    LandscapingExtentionPoints.get_landscape_type)
                LANDSCAPE_SINGLETON = LandscapeType()
        finally:
            SINGLETON_LOCK.release()

    return LANDSCAPE_SINGLETON

