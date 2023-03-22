"""
.. module:: landscapeconfigurationlayer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`LandscapeConfigurationLayer` class which is used
               to load the various configuration files and to provide methods for working with
               configuration information.

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

from typing import Any, Dict, List, Tuple, Union, TYPE_CHECKING

import json
import os
import traceback
import yaml


from mojo.xmods.credentials.credentialmanager import CredentialManager
from mojo.xmods.xcollections.context import Context, ContextPaths
from mojo.xmods.xcollections.mergemap import MergeMap
from mojo.xmods.exceptions import ConfigurationError
from mojo.xmods.xyaml import safe_load_yaml_files_as_mergemap

from mojo.xmods.landscaping.layers.landscapinglayerbase import LandscapingLayerBase

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape


class LandscapeConfigurationLayer(LandscapingLayerBase):
    """
        The base class for all derived :class:`LandscapeDescription` objects.  The
        :class:`LandscapeDescription` is used to load a description of the entities
        and resources in the tests landscape that will be used by the tests.
    """

    def __init__(self, lscape: "Landscape"):
        super().__init__(lscape)

        self._credential_manager: CredentialManager = None

        self._landscape_files: List[str] = None
        self._landscape_info: MergeMap = None

        self._topology_files: List[str] = None
        self._topology_info: MergeMap = None

        # We can get runtime configuration from the global context which
        # should already be loaded
        self._global_context = Context()
        return

    @property
    def credential_manager(self) -> CredentialManager:
        return self._credential_manager
    
    @property
    def landscape_files(self) -> List[str]:
        return self._landscape_files
    
    @property
    def landscape_info(self) -> Union[MergeMap, None]:
        return self._landscape_info

    @property
    def topology_files(self) -> List[str]:
        return self._topology_files
    
    @property
    def topology_info(self) -> Union[MergeMap, None]:
        return self._topology_info


    def initialize_credentials(self) -> None:
        """
            Initialize the credentials manager for the landscape object.
        """
        self._credential_manager = CredentialManager()
        return


    def load_landscape(self) -> Union[MergeMap, None]:
        """
            Loads and validates the landscape description file.
        """

        self._landscape_files = self._global_context.lookup(ContextPaths.CONFIG_LANDSCAPE_FILES, [])

        if len(self._landscape_files):

            self._landscape_info = safe_load_yaml_files_as_mergemap(self._landscape_files, context="Landscape")

            errors, warnings = self.validate_landscape(self._landscape_info)

            if len(errors) > 0:
                errmsg_lines = [
                    "ERROR Landscape validation failures:"
                ]
                for err_path, err_msg in errors:
                    errmsg_lines.append("    {}: {}".format(err_path, err_msg))

                errmsg = os.linesep.join(errmsg_lines)
                raise ConfigurationError(errmsg) from None

            if len(warnings) > 0:
                for wrn_path, wrn_msg in warnings:
                    self.logger.warn("Landscape Configuration Warning: ({}) {}".format(wrn_path, wrn_msg))

        return self._landscape_info


    def load_topology(self) -> Union[MergeMap, None]:
        """
            Loads the topology file.
        """

        self._topology_files = self._global_context.lookup(ContextPaths.CONFIG_TOPOLOGY_FILES, [])

        if len(self._topology_files):

            self._topology_info = safe_load_yaml_files_as_mergemap(self._topology_files, context="Topology")

            errors, warnings = self.validate_topology(self._topology_info)

            if len(errors) > 0:
                errmsg_lines = [
                    "ERROR Topology validation failures:"
                ]
                for err_path, err_msg in errors:
                    errmsg_lines.append("    {}: {}".format(err_path, err_msg))

                errmsg = os.linesep.join(errmsg_lines)
                raise ConfigurationError(errmsg) from None

            if len(warnings) > 0:
                for wrn_path, wrn_msg in warnings:
                    self.logger.warn("Topology Configuration Warning: ({}) {}".format(wrn_path, wrn_msg))

        return self._topology_info


    def record_configuration(self, log_to_directory: str):
        """
            Method code to record the landscape configuration to an output folder
        """
        
        landscape_info_copy = self._landscape_info.flatten()
        landscape_declared_file = None

        try:
            landscape_declared_file = os.path.join(log_to_directory, "landscape-declared.yaml")
            with open(landscape_declared_file, 'w') as lsf:
                yaml.safe_dump(landscape_info_copy, lsf, indent=4, default_flow_style=False)

            landscape_declared_file = os.path.join(log_to_directory, "landscape-declared.json")
            with open(landscape_declared_file, 'w') as lsf:
                json.dump(landscape_info_copy, lsf, indent=4)

        except Exception as xcpt:
            err_msg = "Error while logging the landscape configuration file (%s)%s%s" % (
                landscape_declared_file, os.linesep, traceback.format_exc())
            raise RuntimeError(err_msg) from xcpt
        
        topology_info_copy = self._topology_info.flatten()
        topology_declared_file = None

        try:
            topology_declared_file = os.path.join(log_to_directory, "topology-declared.yaml")
            with open(topology_declared_file, 'w') as lsf:
                yaml.safe_dump(topology_info_copy, lsf, indent=4, default_flow_style=False)

            topology_declared_file = os.path.join(log_to_directory, "topology-declared.json")
            with open(topology_declared_file, 'w') as lsf:
                json.dump(topology_info_copy, lsf, indent=4)

        except Exception as xcpt:
            err_msg = "Error while logging the topology configuration file (%s)%s%s" % (
                topology_declared_file, os.linesep, traceback.format_exc())
            raise RuntimeError(err_msg) from xcpt

        # NOTE: The `LandscapeConfigurationLayer` is not responsible for recording the runtime configuration
        # information.  The loading and recording of runtime configuration is accomplished by the `mojo-runtime`
        # package.

        return


    def validate_landscape(self, landscape_info) -> Tuple[List[str], List[str]]:
        """
            Validates the landscape description file.
        """
        errors = []
        warnings = []

        if "pod" in landscape_info:
            podinfo = landscape_info["pod"]
            for section in podinfo:
                if section == "environment":
                    envinfo = landscape_info["environment"]
                    child_errors, child_warnings = self.validate_landscape_environment(envinfo)
                    errors.extend(child_errors)
                    warnings.extend(child_warnings)
                else:
                    section_items = podinfo[section]
                    errors, warnings = self.validate_landscape_section(section, section_items)
        else:
            errors.append(["/pod", "A landscape description requires a 'pod' data member."])

        return errors, warnings


    def validate_landscape_environment(self, envinfo) -> Tuple[List[str], List[str]]:
        """
        "environment":
            "label": "production"
        """
        errors = []
        warnings = []

        return errors, warnings


    def validate_landscape_section(self, section: str, section_items: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:

        errors = []
        warnings = []

        lscape: "Landscape" = self.landscape

        remaining_items = [item for item in section_items]

        for nxt_coupling_type in lscape.installed_integration_couplings.values():

            if nxt_coupling_type.integration_section == section:
                validated_items = []

                for nxt_item in remaining_items:
                    if nxt_coupling_type.integration_leaf in nxt_item:
                        nxt_class = nxt_item[nxt_coupling_type.integration_leaf]
                        if nxt_class == nxt_coupling_type.integration_class:
                            ierrors, iwarnings = nxt_coupling_type.validate_item_configuration(nxt_item)
                            errors.extend(ierrors)
                            warnings.extend(iwarnings)
                            validated_items.append(nxt_item)

                for item in validated_items:
                    remaining_items.remove(item)

        return errors, warnings


    def validate_runtime(self, runtime_info: dict) -> Tuple[List[str], List[str]]:
        """
            Validates the runtime configuration.
        """
        errors = []
        warnings = []

        return errors, warnings


    def validate_topology(self, topology_info: dict) -> Tuple[List[str], List[str]]:
        """
            Validates the topology configuration.
        """
        errors = []
        warnings = []

        return errors, warnings

