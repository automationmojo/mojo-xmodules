
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Callable, Dict, Optional, Type

import inspect

from types import TracebackType

from mojo.errors.exceptions import SemanticError

from mojo.xmods.injection.resourceregistry import resource_registry

from mojo.xmods.injection.resourcelifespan import ResourceLifespan
from mojo.xmods.injection.validatororigin import ValidatorOrigin
from mojo.xmods.injection.parameterorigin import ParameterOrigin

from mojo.xmods.xinspect import is_typed_from_type

def param(source, *, identifier: Optional[None], constraints: Optional[Dict]=None):
    def decorator(subscriber: Callable) -> Callable:
        nonlocal source
        nonlocal identifier
        nonlocal constraints

        if identifier is None:
            identifier = source.__name__

        if identifier == 'constraints':
            errmsg = "Invalid identifier.  The word 'constraints' is reseved for delivering dynamic constraints."
            raise SemanticError(errmsg) from None

        life_span = ResourceLifespan.Test

        source_info = resource_registry.lookup_resource_source(source)

        if constraints is not None and 'constraints' not in source_info.source_signature.parameters:
            raise SemanticError("Attempting to pass constraints to a parameter origin with no 'constraints' parameter.") from None

        assigned_scope = "{}#{}".format(subscriber.__module__, subscriber.__name__)

        param_origin = ParameterOrigin(assigned_scope, identifier, life_span, source_info, constraints)
        resource_registry.register_parameter_origin(identifier, param_origin)

        return subscriber
    return decorator

def validator(source, *, identifier: Optional[None], constraints: Optional[Dict]=None):
    def decorator(subscriber: Callable) -> Callable:
        nonlocal source
        nonlocal identifier
        nonlocal constraints

        if identifier is None:
            identifier = source.__name__

        if identifier == 'constraints':
            errmsg = "Invalid identifier.  The word 'constraints' is reseved for delivering dynamic constraints."
            raise SemanticError(errmsg) from None

        source_info = resource_registry.lookup_resource_source(source)

        if constraints is not None and 'constraints' not in source_info.source_signature.parameters:
            raise SemanticError("Attempting to pass constraints to a parameter origin with no 'constraints' parameter.") from None

        assigned_scope = "{}#{}".format(subscriber.__module__, subscriber.__name__)

        param_origin = ValidatorOrigin(assigned_scope, identifier, source_info, constraints)
        resource_registry.register_validator_origin(identifier, param_origin)

        return subscriber
    return decorator