"""
.. module:: resources
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: A set of standardized decorations that are utilized to declare integrations
               scope and resource factory functions.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []



from typing import Callable, Dict, Optional, TypeVar

import inspect
import os

NoneType = type(None)

from mojo.xmods.injection.coupling.integrationcoupling import IntegrationCoupling
from mojo.xmods.injection.coupling.scopecoupling import ScopeCoupling

from mojo.errors.exceptions import SemanticError

from mojo.xmods.injection.injectionregistry import injection_registry

from mojo.xmods.injection.integrationsource import IntegrationSource
from mojo.xmods.injection.resourcesource import ResourceSource
from mojo.xmods.injection.scopesource import ScopeSource
from mojo.xmods.injection.coupling.validatorcoupling import ValidatorCoupling
from mojo.xmods.injection.validatorsource import ValidatorSource

_IntegrationSubscriberType = TypeVar("_IntegrationSubscriberType", bound=Callable[..., object])

def integration(*, constraints: Optional[Dict]=None):
    """
        The `integration` decorator is used to declare a function as the source
        of an integration resource.
    """
    def decorator(source_function: Callable) -> Callable:
        nonlocal constraints

        signature = inspect.signature(source_function)
        integration_context = signature.return_annotation

        resource_type = None

        if integration_context == inspect._empty:
            errmsg = "Parameters factories for 'integration' functions must have an annotated return type."
            raise SemanticError(errmsg) from None
        else:
            if integration_context._name == "Generator":
                ra_yield_type, ra_send_type, ra_return_type = integration_context.__args__
                if ra_yield_type is not NoneType:
                    resource_type = ra_yield_type
                elif ra_return_type is not NoneType:
                    resource_type = ra_return_type
            elif issubclass(integration_context, IntegrationCoupling):
                raise SemanticError("Your resource function is returning an integration instead of yielding one.") from None
            else:
                raise SemanticError("You must pass a IntegrationCoupling derived object.") from None

        if resource_type is not None:

            if not issubclass(resource_type, IntegrationCoupling):
                raise SemanticError("The 'integration' decorator can only be used on resources that inherit from the 'IntegrationCoupling'.") from None

            isource = IntegrationSource(source_function, resource_type, constraints)
            injection_registry.register_integration_source(isource)
        else:
            errmsg_lines = [
                "Unable to determine the resource type of the function which the 'integration' decorator was applied too.",
                "FUNCTION: {}".format(signature)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise SemanticError(errmsg) from None

        return source_function
    return decorator

def resource(*, query_function: Optional[Callable]=None, constraints: Optional[Dict]=None):
    def decorator(source_function: Callable) -> Callable:
        nonlocal constraints

        signature = inspect.signature(source_function)
        resource_context = signature.return_annotation

        resource_type = None

        if resource_context == inspect._empty:
            errmsg = "Parameters factories or 'resource' functions must have an annotated return type."
            raise SemanticError(errmsg) from None
        elif hasattr(resource_context, "_name") and resource_context._name == "Generator":
            ra_yield_type, ra_send_type, ra_return_type = resource_context.__args__
            if ra_yield_type is not NoneType:
                resource_type = ra_yield_type
            elif ra_return_type is not NoneType:
                resource_type = ra_return_type
        elif issubclass(resource_context, IntegrationCoupling):
            resource_type = resource_context
        else:
            resource_type = resource_context
        
        if resource_type is not None:

            sref = ResourceSource(source_function, query_function, resource_type, constraints)
            injection_registry.register_resource_source(sref)
        else:
            errmsg_lines = [
                "Unable to determine the resource type of the function which the 'resource' decorator was applied too.",
                "FUNCTION: {}".format(signature)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise SemanticError(errmsg) from None

        return source_function
    return decorator

def scope(*, query_function: Optional[Callable]=None, constraints: Optional[Dict]=None):
    """
        The `scope` decorator is used to declare a function as the source
        of an scope resource.
    """
    def decorator(source_function: Callable) -> Callable:
        nonlocal constraints

        signature = inspect.signature(source_function)
        scope_context = signature.return_annotation

        resource_type = None

        if scope_context == inspect._empty:
            errmsg = "Parameters factories or 'scope' functions must have an annotated return type."
            raise SemanticError(errmsg) from None
        elif scope_context._name == "Generator":
            ra_yield_type, ra_send_type, ra_return_type = scope_context.__args__
            if ra_yield_type is not NoneType:
                resource_type = ra_yield_type
            elif ra_return_type is not NoneType:
                resource_type = ra_return_type
        elif issubclass(scope_context, ScopeCoupling):
            resource_type = scope_context
        else:
            raise SemanticError("You must pass a ScopeCoupling derived object.") from None
        
        if resource_type is not None:

            if not issubclass(resource_type, ScopeCoupling):
                raise SemanticError("The 'scope' decorator can only be used on resources that inherit from the 'scopecoupling'.") from None

            ssource = ScopeSource(source_function, query_function, resource_type, constraints)
            injection_registry.register_scope_source(ssource)
        else:
            errmsg_lines = [
                "Unable to determine the resource type of the function which the 'scope' decorator was applied too.",
                "FUNCTION: {}".format(signature)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise SemanticError(errmsg) from None

        return source_function
    return decorator

def validator(*, constraints: Optional[Dict]=None):
    def decorator(source_function: Callable) -> Callable:
        nonlocal constraints

        signature = inspect.signature(source_function)
        resource_context = signature.return_annotation

        resource_type = None

        if resource_context == inspect._empty:
            errmsg = f"Validator factories must have an annotated return type. resource_context={resource_context}"
            raise SemanticError(errmsg) from None
        elif issubclass(resource_context, ValidatorCoupling):
            resource_type = resource_context
        else:
            errmsg = f"Validator factory functions must have a return type that is subclassed from 'ValidatorBase'. resource_context={resource_context}"
            raise SemanticError(errmsg) from None
        
        sref = ValidatorSource(source_function, resource_type, constraints)
        injection_registry.register_validator_source(sref)
        
        return source_function
    return decorator