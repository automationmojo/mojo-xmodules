
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import (
    Any, Callable, Dict, List, get_args as typing_get_args
)

import collections

from mojo.errors.exceptions import SemanticError
from mojo.xmods.landscaping.coupling.integrationcoupling import IntegrationCoupling
from mojo.xmods.landscaping.coupling.scopecoupling import ScopeCoupling

from mojo.xmods.injection.parameterorigin import ParameterOrigin

from mojo.xmods.injection.injectableref import InjectableRef

RESOURCE_KEY_FORMAT = "{}@{}:{}"

RESERVED_PARAMETER_NAMES = ["constraints"]

class ResourceScope:

    def __init__(self, name=None, package=None, is_inj_scope=False):
        self._name = name
        self._package = package
        self._children: Dict[str, ResourceScope] = {}
        self._parameter_originations = collections.OrderedDict()
        self._is_inj_scope = is_inj_scope
        self._is_relevant = False
        return

    @property
    def children(self) -> Dict[str, "ResourceScope"]:
        return self._children

    @property
    def is_relevant(self) -> bool:
        return self._is_relevant

    @property
    def name(self) -> str:
        return self._name

    @property
    def package(self) -> str:
        return self._package

    @property
    def parameter_originations(self) -> Dict[str, ParameterOrigin]:
        return self._parameter_originations

    def add_descendent_parameter_origination(self, assigned_scope: str, parameter_origin: ParameterOrigin):
        """
            Adds a descendent parameter origin object into the parameter origin table of the
            assigned scope path provided.

            :param assigned_scope: The full scope name of the scope to assign the parameter
                                   origin to.
            :param parameter_origin: The parameter origin object that is being inserted into
                                     the parameter origin table of the assigned scope.
        """

        if self._package is not None:
            err_msg = "The 'add_descendent' API can only be called on the root package."
            raise SemanticError(err_msg) from None

        if self._package is None and assigned_scope == "<session>":
            if parameter_origin is not None:
                identifier = parameter_origin.identifier
                self._parameter_originations[identifier] =  parameter_origin
                self._parameter_originations.move_to_end(identifier, last=True)
        else:
            is_inj_scope = False
            if assigned_scope.find("#") > -1:
                is_inj_scope = True
                assigned_scope = assigned_scope.replace("#", ".")
            to_walk_list = assigned_scope.split(".")
            path_stack = []

            self._add_descendent_parameter_origination(parameter_origin, to_walk_list, path_stack, is_inj_scope)

        return

    def collect_integrations_and_scopes_for_injectable(self, integration_table: Dict[Callable, IntegrationCoupling],
        scope_table: Dict[Callable, ScopeCoupling]):
        """
            Walk the scope tree path for the injectable reference provide and collect all the integration and
            scope couplings that are referenced along the path.
        """

        param_orig: ParameterOrigin

        for param_orig in self._parameter_originations.values():

            source_function = param_orig.source_function
            param_resource_type = param_orig.source_resource_type

            if len(typing_get_args(param_resource_type)) > 0:
                for type_arg in typing_get_args(param_resource_type):
                    if issubclass(type_arg, IntegrationCoupling):
                        # There should never be more than one fixture with the same well-known or
                        # declared name in the same collection of injectables.
                        integration_table[source_function] = type_arg
                        break
                    elif issubclass(type_arg, ScopeCoupling):
                        scope_table[source_function] = type_arg
                        break
            else:
                if issubclass(param_resource_type, IntegrationCoupling):
                    # There should never be more than one fixture with the same well-known or
                    # declared name in the same collection of injectables.
                    integration_table[source_function] = param_resource_type
                elif issubclass(param_resource_type, ScopeCoupling):
                    scope_table[source_function] = param_resource_type

        for child_scope in self._children.values():

            # Call each child and collect descendant integrations and scopes.
            child_scope.collect_integrations_and_scopes_for_injectable(integration_table, scope_table)

        return

    def ensure_parameter_scopes_for_injectable(self, inj_ref: InjectableRef):
        """
            Walks through the scope tree using the full scope name of a injectable reference
            object and esures there is a scope node for each component of the injectable reference
            path name.

            :param inj_ref: The :class:`InjectableRef` object that ancestrial scope nodes should
                             be created for.
        """

        inj_scope_name = inj_ref.scope_name

        module_name, inj_name = inj_scope_name.split("#")

        inj_scope_parts = module_name.split(".")
        inj_scope_parts.append(inj_name)

        path_stack = []

        self._is_relevant = True
        self._ensure_parameter_scopes_for_injectable(inj_ref, inj_scope_parts, path_stack)

        return

    def has_descendent_parameter(self, scope_name: str, identifier: str) -> bool:
        """
            Method used to findout if the specified scope has a parameter or not
            available 

            :param scope_name: The full path of the scope name to lookup.
            :param identifier: The name of the identifier to search for.
        """

        rtnval = False

        if self._package is None and scope_name == "<session>":
            if identifier in self._parameter_originations:
                rtnval = True
        else:
            scope_name = scope_name.replace("#", ".")
            to_walk_list = scope_name.split(".")

            rtnval = self._has_descendent_parameter(to_walk_list, identifier)

        return rtnval

    def lookup_scope(self, scope_name: str) -> "ResourceScope":
        """
            Method used to parse a full scope name into components and then lookup
            the specified scope in the scope tree.

            :param scope_name: The full path of the scope name to lookup.
        """

        scope_found = None
        if self._package is None and scope_name == "<session>":
            scope_found = self
        else:
            scope_name = scope_name.replace("#", ".")
            to_walk_list = scope_name.split(".")

            if len(to_walk_list) > 0:
                scope_found = self._lookup_scope(to_walk_list)

        return scope_found

    def prune_unreference_scopes(self):
        """
            Walk through all of the child nodes and prune any not relevant scope nodes
            and any of thier descendants.
        """

        temp_child_key_list = [csk for csk in self._children.keys()]
        while len(temp_child_key_list) > 0:
            nxt_child_key = temp_child_key_list.pop()
            nxt_child = self._children[nxt_child_key]

            # Have this child prune its children before we prune it
            # from this nodes children table
            if len(nxt_child._children) > 0:
                nxt_child.prune_unreference_scopes()

            # If we had this child prune its children, then we can
            # prune this child.
            if not nxt_child._is_relevant:
                del self._children[nxt_child_key]

        return

    def rename_resource_origins_from_main(self, new_origin: str):
        """
        """

        if "__main__" in self._children:
            last_dot = new_origin.rfind(".")

            cobj = self._children["__main__"]
            del self._children["__main__"]

            self._children[new_origin] = cobj

            # All of the children of cobj will be injectables, go through all of
            # the child objects and fix the package name
            for inj_scope in cobj._children.values():
                inj_scope_origin = "{}#{}".format(new_origin, inj_scope._name)
                for _, poval in inj_scope.parameter_originations.items():
                    poval._originating_scope = inj_scope_origin
                    self.add_descendent_parameter_origination(inj_scope_origin, poval)

        return

    def resolve_parameter_originations_for_injectable(self, inj_ref: InjectableRef, missing_params: List[Any]):
        """
            Walk through all the descendant nodes of this node utilizing the injectable reference
            full scope name for a path and validate the resolution of all parameters that are
            being utilized by any parameter source functions or any of thier sources.

            :param inj_ref: The :class:`InjectableRef` object whos scope path is used to validate a
                             single scope path from the set of all parameter scope paths.
            :param missing_params: The list of parameters that are found to be missing when
                                   searching the descent of the scope path.
        """

        inj_scope_name = inj_ref.scope_name

        module_name, inj_name = inj_scope_name.split("#")

        inj_scope_parts = module_name.split(".")
        inj_scope_parts.append(inj_name)

        param_table = {}
        for pname, pinfo in self._parameter_originations.items():
            param_table[pname] = pinfo

        self._resolve_parameter_originations_for_injectable_descend(inj_ref, inj_scope_parts, param_table, missing_params)

        return

    def _add_descendent_parameter_origination(self, parameter_origin: ParameterOrigin, to_walk_list: List[str], path_stack: List[str], is_inj_scope):

        curr_leaf = to_walk_list.pop(0)
        curr_scope = None

        if curr_leaf in self._children:
            curr_scope = self._children[curr_leaf]
        else:
            curr_package = curr_leaf
            if len(path_stack) > 0:
                curr_package = "{}.{}".format(".".join(path_stack), curr_package)

            set_inj_scope = False
            if len(to_walk_list) == 0:
                set_inj_scope = is_inj_scope

            curr_scope = ResourceScope(curr_leaf, curr_package, set_inj_scope)
            self._children[curr_leaf] = curr_scope

        if len(to_walk_list) > 0:
            path_stack.append(curr_leaf)
            curr_scope._add_descendent_parameter_origination(parameter_origin, to_walk_list, path_stack, is_inj_scope)
            path_stack.pop()
        else:
            if parameter_origin is not None:
                identifier = parameter_origin.identifier
                curr_scope._parameter_originations[identifier] = parameter_origin
                curr_scope._parameter_originations.move_to_end(identifier, last=True)

        return

    def _ensure_parameter_scopes_for_injectable(self, inj_ref: InjectableRef, inj_scope_parts: List[str], path_stack: List[str]):

        if len(inj_scope_parts) > 0:
            curr_leaf = inj_scope_parts.pop(0)

            if curr_leaf not in self._children:
                curr_package = curr_leaf
                if len(path_stack) > 0:
                    curr_package = "{}.{}".format(".".join(path_stack), curr_package)
                
                set_inj_scope = False
                if len(inj_scope_parts) == 0:
                    set_inj_scope = True
                curr_scope = ResourceScope(curr_leaf, curr_package, set_inj_scope)
                curr_scope._is_relevant = True
                self._children[curr_leaf] = curr_scope

                path_stack.append(curr_leaf)
                curr_scope = self._children[curr_leaf]
                curr_scope._ensure_parameter_scopes_for_injectable(inj_ref, inj_scope_parts, path_stack)

            else:
                path_stack.append(curr_leaf)
                curr_scope = self._children[curr_leaf]
                curr_scope._is_relevant = True
                curr_scope._ensure_parameter_scopes_for_injectable(inj_ref, inj_scope_parts, path_stack)

        return

    def _has_descendent_parameter(self, to_walk_list: List[str], identifier: str):

        rtnval = False

        if len(to_walk_list) == 0:
            if identifier in self._parameter_originations:
                rtnval = True
        else:
            child_name = to_walk_list[0]
            if child_name in self._children:
                scope = self._children[child_name]
                desc_to_walk_list = to_walk_list[1:]
                rtnval = scope._has_descendent_parameter(desc_to_walk_list, identifier)

        return rtnval

    def _lookup_scope(self, to_walk_list: List[str]) -> "ResourceScope":
        """
            The private recursive method for lookup_scope that is used to find a scope by path
            in the scope tree.

            :param to_walk_list: A list of scope names to walk down to find the desired scope.
        """

        scope_found = None

        child_name = to_walk_list.pop(0)
        if child_name in self._children:
            child_scope = self._children[child_name]
            if len(to_walk_list) > 0:
                scope_found = child_scope._lookup_scope(to_walk_list)
            else:
                scope_found = child_scope

        return scope_found

    def _resolve_parameter_originations_for_injectable_descend(self, inj_ref: InjectableRef, inj_scope_parts: List[str],
        param_table: dict, missing_params: List[Any]):

        if len(inj_scope_parts) > 0:
            nxt_scope_name = inj_scope_parts.pop(0)
            if nxt_scope_name in self._children:
                nxt_scope = self._children[nxt_scope_name]

                nxt_param_table = param_table.copy()

                # Go through all the parameter originations registered in this scope an add them
                # to the nxt_param_table dictionary to pass down to descendant scopes
                origination_items = [(spn, spo) for spn, spo in nxt_scope.parameter_originations.items()]
                for scope_param_name, scope_param_origin in origination_items:
                    
                    if isinstance(scope_param_origin, ParameterOrigin):
                        # Do a lateral check to make sure the originating methods of any declared parameters
                        # already have parameters declared in the current in scope parameters
                        self._resolve_parameter_originations_for_injectable_lateral(inj_ref, scope_param_origin,
                            inj_scope_parts, nxt_param_table, missing_params)

                        # Add the new parameter origination to the parameter lookup table for this scope as
                        # it came first and can feed any following parameter source.
                        nxt_param_table[scope_param_name] = scope_param_origin
                    else:
                        print("{}:{}".format(nxt_scope.package, scope_param_name))

                nxt_scope._resolve_parameter_originations_for_injectable_descend(inj_ref, inj_scope_parts, nxt_param_table, missing_params)
            else:
                print("child not found '{}'".format(nxt_scope_name))
        return

    def _resolve_parameter_originations_for_injectable_lateral(self, inj_ref: InjectableRef, lateral_param_origin: ParameterOrigin,
        inj_scope_parts: List[str], scope_param_table: dict, missing_params: List[Any]):

        source_params = lateral_param_origin.source_signature.parameters
        if len(source_params) > 0:
            for sparam_name, sparam_origin in source_params.items():
                if sparam_name not in scope_param_table and sparam_name not in RESERVED_PARAMETER_NAMES:
                    missing_params.append([sparam_name, sparam_origin])
        return

