
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


from typing import Callable, Union, Type

from mojo.xmods.injection.sourcebase import SourceBase

class ResourceSource(SourceBase):

    def __init__(self, source_func: Callable, query_func: Union[Callable, None], resource_type: Type, constraints: dict):
        SourceBase.__init__(self, source_func, query_func, resource_type, constraints)
        return
