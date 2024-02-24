
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Any, Callable, Dict, Optional, Type, Union

import inspect

from mojo.xmods.injection.constraintscatalog import ConstraintsCatalog
from mojo.xmods.injection.constraints import ConstraintsOrigin
from mojo.xmods.injection.sourcebase import SourceBase
from mojo.xmods.injection.resourcelifespan import ResourceLifespan

constraints_catalog = ConstraintsCatalog()

class ValidatorOrigin:

    def __init__(self, originating_scope: str, identifier: str, suffix: str, source: Optional[SourceBase] = None, implied: bool = False, constraints: Optional[Dict] = None):
        self._originating_scope = originating_scope
        self._identifier = identifier
        self._suffix = suffix
        self._life_span = ResourceLifespan.Test
        self._source = source
        self._implied = implied
        
        self._constraints_key = None
        if constraints is not None:
            self._constraints_key = constraints_catalog.add_constraints(ConstraintsOrigin.SITE_PARAMETER, originating_scope, identifier, constraints)
        return

    @property
    def constraints_key(self) -> str:
        return self._constraints_key

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def implied(self) -> bool:
        return self._implied

    @property
    def life_span(self) -> ResourceLifespan:
        return self._life_span

    @property
    def originating_scope(self) -> str:
        return self._originating_scope

    @property
    def source_function(self) -> Callable:
        return self._source.source_function

    @property
    def source_function_name(self) -> str:
        return self._source.source_function.__name__

    @property
    def source_signature(self) -> inspect.Signature:
        return self._source.source_signature

    @property
    def source_id(self) -> str:
        idstr = self._source.source_id
        return idstr

    @property
    def source_module_name(self) -> str:
        return self._source.module_name

    @property
    def source_resource_type(self) -> Type:
        return self._source.resource_type

    @property
    def suffix(self) -> str:
        return self._suffix

    def describe_source(self):
        descstr = self.source_id
        return descstr

    def generate_call(self, constraints: Optional[dict] = None):
        call_arg_str = ""

        call_args = [param for param in self.source_signature.parameters]
        if constraints is None and "constraints" in call_args:
            call_args.remove("constraints")

        if len(call_args) > 0:
            call_arg_str = ", ".join(call_args)

        call_str = "{}({})".format(self._source.source_function.__name__, call_arg_str)
        
        return call_str