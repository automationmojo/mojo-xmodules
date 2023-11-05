
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Callable, Type

from mojo.xmods.injection.sourcebase import SourceBase

class UnknownSource(SourceBase):
    """
        The :class:`UnknownSource` object is used when a parameter is declared for a
        injectable method of other resource function that cannot be resolved to a source
        function.  The :class:`UnknownSource` enables the injectable parameters to be queried
        by acting as a placeholder.
    """
    def __init__(self, source_func: Callable, resource_type: Type, constraints: dict):
        SourceBase.__init__(self, source_func, resource_type, constraints)
        return
