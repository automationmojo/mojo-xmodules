"""
.. module:: injectablegroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`InjectableGroup` class which is utilized as the collection point
               which associates a set of injectables with their descendant execution scopes.

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

from typing import Dict, List, Optional, Union

import logging
import sys

from mojo.errors.exceptions import SemanticError

from mojo.xmods.injection.resourceregistry import resource_registry
from mojo.xmods.injection.resourcescope import ResourceScope

from mojo.xmods.injection.injectableref import InjectableRef

logger = logging.getLogger()

class InjectableGroup:
    """
              -------------
              |  Group A  |
        ---------------------------
        |  Group AA  |  Scope AB  |
        -------------------------------
        |         Scope AAA/ABA       |
        -------------------------------
    """

    def __init__(self, name, package=None):
        self._name = name
        self._package = package
        self._children = {}
        self._finalized = False
        self._metadata = None
        return

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        return False

    @property
    def children(self):
        return self._children

    @property
    def finalized(self):
        return self._finalized

    @property
    def name(self):
        return self._name

    @property
    def package(self):
        return self._package

    @property
    def scope_name(self):
        sname = self._name
        if self._package is not None and len(self._package) > 0:
            sname = "{}.{}".format(self.package, sname)
        return sname

    def add_descendent(self, child_ref:InjectableRef, group_type: Optional[type] = None):

        if self._package is not None:
            err_msg = "The 'add_descendent' API can only be called on the root package."
            raise SemanticError(err_msg) from None

        injname = child_ref.name
        module_name, _ = injname.split("#")
        to_walk_list = module_name.split(".")
        path_stack = []

        self._add_descendent(child_ref, to_walk_list, path_stack, group_type=group_type)

        return

    def finalize(self):
        self._finalized = True
        return

    def get_resource_scope(self) -> ResourceScope:
        scope_name = self.scope_name
        rscope = resource_registry.lookup_resource_scope(scope_name)
        return rscope

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

        child: Union[InjectableRef, InjectableGroup]
        for child in self._children.values():
            child.resolve_metadata(self._metadata)

        return

    def _add_descendent(self, child_ref: InjectableRef, to_walk_list: List[str], path_stack: List[str], group_type: Optional[type] = None):
        
        if len(to_walk_list) == 0:
            tbname = child_ref.base_name
            self._children[tbname] = child_ref
        else:
            child_leaf = to_walk_list[0]

            desc_to_walk_list = []
            if len(to_walk_list) > 1:
                desc_to_walk_list = to_walk_list[1:]

            child_leaf_group = None
            if child_leaf in self._children:
                child_leaf_group = self._children[child_leaf]
            else:
                if group_type is None:
                    group_type = type(self)

                tgname = child_leaf
                tgpkg = ".".join(path_stack) 

                child_leaf_group = group_type(tgname, tgpkg)
                self._children[child_leaf] = child_leaf_group

            path_stack.append(child_leaf)
            try:
                child_leaf_group._add_descendent(child_ref, desc_to_walk_list, path_stack)
            finally:
                path_stack.pop()

        return

    def _reference_metadata(self):
        """
            Looks up the metadata if any on the module associated with this group.
        """
        
        modname = self._name
        if self._package is not None and self._package != "":
            modname = "{}.{}".format(self._package, self._name)

        refmd = None
        if modname in sys.modules:
            mod = sys.modules[modname]
            if hasattr(mod, "_metadata_"):
                refmd = mod._metadata_

        return refmd

    def __contains__(self, key):
        has_item = key in self._children
        return has_item

    def __getitem__(self, key):
        item = self._children[key]
        return item

    def __setitem__(self, key, value):
        self._children[key] = value
        return
