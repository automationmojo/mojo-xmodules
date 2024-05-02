
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"


from typing import Callable, Type

from mojo.xmods.injection.sourcebase import SourceBase

class ValidatorSource(SourceBase):

    def __init__(self, source_func: Callable, resource_type: Type, constraints: dict):
        SourceBase.__init__(self, source_func, None, resource_type, constraints)
        return
