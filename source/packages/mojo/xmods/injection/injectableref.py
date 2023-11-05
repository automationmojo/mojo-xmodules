"""
.. module:: injectableref
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the base :class:`InjectableRef` type used to reference to
        injectable function that will be included into an a execution graph.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Any, Dict, List, OrderedDict, Optional, Sequence

from types import FunctionType

import collections
import inspect
import sys

from mojo.xmods.markers import MetaFilter

class InjectableRef:
    """
        The :class:`InjectableRef` objects are used to refer to a reference to a injectable.  We use :class:`InjectableRef` instances
        to reference the function that are going to be run so we can control the lifespan of an injectable function instances
        and control our memory consumption during execution runs with large collections of injectables.

        The :class:`InjectableRef` object allows us to delay the creation of injectable runtime instance data and state until it is
        necessary to instantiate it and allows us to cleanup the runtime instance and state as soon as it is no longer
        being used.
    """

    def __init__(self, injfunc: FunctionType, monikers: List[str]=[], pivots: OrderedDict[str, Any]=collections.OrderedDict()):
        """
            Initializes the injectable reference object.
        """
        self._inj_function = injfunc
        self._monikers = monikers
        self._pivots = pivots
        self._subscriptions = {}
        self._finalized = False
        return

    @property
    def finalized(self) -> bool:
        return self._finalized

    @property
    def monikers(self) -> List[str]:
        return self._monikers

    @property
    def pivots(self) -> OrderedDict[str, Any]:
        return self._pivots

    @property
    def scope_name(self) -> str:
        return self.name

    @property
    def subscriptions(self):
        return self._subscriptions

    @subscriptions.setter
    def subscriptions(self, val):
        self._subscriptions = val
        return

    @property
    def base_name(self) -> str:
        tbname = self._inj_function.__name__
        return tbname

    @property
    def function(self) -> FunctionType:
        """
            The injectable function 
        """
        return self._inj_function

    @property
    def function_parameters(self):
        signature = inspect.signature(self._inj_function)
        return signature.parameters

    @property
    def module_name(self) -> str:
        return self._inj_function.__module__

    @property
    def name(self) -> str:
        """
            The fully qualified name of the injectable that is referenced.
        """
        tf = self._inj_function
        inj_name = "%s#%s" % (tf.__module__, tf.__name__)
        return inj_name

    def finalize(self):
        self._finalized = True
        return

    def is_member_of_metaset(self, metafilters: Sequence[MetaFilter]):
        """
            Indicates if a injectable belongs to a set that is associated with a collection of metafilters.
        """
        include = True

        for mfilter in metafilters:
            if not mfilter.should_include(self._metadata):
                include = False

        return include

    def resolve_metadata(self, parent_metadata: Optional[Dict[str, str]]=None):

        reference_metadata = self._reference_metadata()

        if parent_metadata is not None:
            if reference_metadata is not None:
                self._metadata = {}
                self._metadata.update(parent_metadata)
                self._metadata.update(reference_metadata)
            else:
                self._metadata = parent_metadata
        else:
            self._metadata = reference_metadata

        return

    def _reference_metadata(self):
        """
            Looks up the metadata if any on the module associated with this group.
        """
        
        refmd = None
        if hasattr(self._inj_function, "_metadata_"):
            refmd = self._inj_function._metadata_

        return refmd

    def __str__(self):
        return self.name
