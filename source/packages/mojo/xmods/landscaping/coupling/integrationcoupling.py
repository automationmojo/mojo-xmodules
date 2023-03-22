"""
.. module:: integration
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`IntegrationCoupling` class and associated reflection methods.
        The :class:`IntegrationCoupling` derived classes can be used to integraton automation resources and roles
        into the test environment.

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

from typing import Any, Dict, List, Tuple, TypeVar, TYPE_CHECKING

import inspect

from mojo.xmods.landscaping.coupling.basecoupling import BaseCoupling
from mojo.xmods.exceptions import NotOverloadedError

from mojo.xmods.landscaping.friendlyidentifier import FriendlyIdentifier
from mojo.xmods.landscaping.landscapedevice import LandscapeDevice

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape

class IntegrationCoupling(BaseCoupling):
    """
        The :class:`IntegrationCoupling` object serves as the base object for the declaration of an
        automation integration requirement.  The :class:`akit.testing.unittest.testsequencer.Sequencer`
        queries the class hierarchies of the tests that are included in an automation run.
    """

    landscape: "Landscape" = None

    integration_section: str = None
    integration_leaf: str = None
    integration_class: str = None

    integrated_devices: List[LandscapeDevice] = []

    def __init__(self, *args, **kwargs): # pylint: disable=unused-argument
        """
            The default contructor for an :class:`IntegrationCoupling`.
        """
        super().__init__()

        self._connectivity_establish = False
        self._presence_establish = False

        return

    @property
    def connectivity_establish(self):
        return self._connectivity_establish

    @property
    def presence_establish(self):
        return self._presence_establish

    @classmethod
    def declare_precedence(cls) -> int:
        """
            This API is called so that the IntegrationCoupling can declare an ordinal precedence that should be
            utilized for bringing up its integration state.
        """
        return

    @classmethod
    def attach_to_environment(cls, constraints: Dict={}):
        """
            This API is called so that the IntegrationCoupling can process configuration information.  The :class:`IntegrationCoupling`
            will verify that it has a valid environment and configuration to run in.

            :raises :class:`akit.exceptions.AKitMissingConfigError`, :class:`akit.exceptions.AKitInvalidConfigError`:
        """
        errmsg = "The 'attach_to_environment' method must be overloaded by derived integration coupling types."
        raise NotOverloadedError(errmsg)
    
    @classmethod
    def attach_to_framework(cls, landscape: "Landscape"):
        """
            This API is called so that the IntegrationCoupling can attach to the test framework and participate with
            registration processes.  This allows the framework to ignore the bring-up of couplings that are not being
            included by a test.
        """
        cls.landscape = landscape
        return

    @classmethod
    def collect_resources(cls):
        """
            This API is called so the `IntegrationCoupling` can connect with a resource management
            system and gain access to the resources required for the automation run.

            :raises :class:`akit.exceptions.AKitResourceError`:
        """
        errmsg = "The 'collect_resources' method must be overloaded by derived integration coupling types."
        raise NotOverloadedError(errmsg)

    @classmethod
    def create_landscape_device(cls, device_info: Dict[str, Any]) -> Tuple[FriendlyIdentifier, LandscapeDevice]:
        """
            Device called by the :class:`LandscapeConfigurationLayer` for devices associated with a specified
            device integration as specified by the `deviceType` field of a device declaration.

            ..note: When implementing this method, the devices created by an integration coupling should be added to
                    the `integrated_devices` list attached to this class.  The integration coupling can inherit
                    from :class:`LandscapeDevice` in order to provide a more device characteristic base type.
            
            ..note: The device created at this point in the startup process are generally generic base versions of
                    a given device type.  These generic versions can later be swapped out for more specific versions
                    once connectivity has been established with the device.
        """

        errmsg = "The 'create_landscape_device' method must be overloaded by derived integration coupling types."
        raise NotOverloadedError(errmsg)

    @classmethod
    def diagnostic(cls, label: str, level: int, diag_folder: str): # pylint: disable=unused-argument
        """
            The API is called by the :class:`akit.sequencer.Sequencer` object when the automation sequencer is
            building out a diagnostic package at a diagnostic point in the automation sequence.  Example diagnostic
            points are:

            * pre-run
            * post-run

            Each diagnostic package has its own storage location so derived :class:`akit.scope.ScopeCoupling` objects
            can simply write to their specified output folder.

            :param label: The label associated with this diagnostic.
            :param level: The maximum diagnostic level to run dianostics for.
            :param diag_folder: The output folder path where the diagnostic information should be written.
        """
        return

    @classmethod
    def establish_connectivity(cls, allow_missing_devices: bool=False) -> Tuple[List[str], Dict]:
        """
            This API is called so the `IntegrationCoupling` can establish connectivity with any compute or storage
            resources.

            :param allow_missing_devices: Boolean indicating if missing devices should be allowed

            :returns: A tuple with a list of error messages for failed connections and dict of connectivity
                      reports for devices devices based on the coordinator.
        """
        errmsg = "The 'diagnostic' method must be overloaded by derived integration coupling types."
        raise NotOverloadedError(errmsg)

    @classmethod
    def establish_presence(cls) -> Tuple[List[str], Dict]:
        """
            This API is called so the `IntegrationCoupling` can establish presence with any compute or storage
            resources.

            :returns: A tuple with a list of error messages for failed connections and dict of connectivity
                      reports for devices devices based on the coordinator.
        """
        errmsg = "The 'diagnostic' method must be overloaded by derived integration coupling types."
        raise NotOverloadedError(errmsg)

    @classmethod
    def validate_item_configuration(cls, item_info: Dict[str, Any]):
        errmsg = "The 'validate_item_configuration' method must be overloaded by derived integration coupling types."
        raise NotOverloadedError(errmsg)

IntegrationCouplingType = TypeVar('IntegrationCouplingType', bound=IntegrationCoupling)

def is_integration_coupling(cls):
    """
        Helper function that is used to determine if a type is an :class:`IntegrationCoupling` subclass, but not
        the :class:`IntegrationCoupling` type itself.
    """
    is_integmi = False
    if inspect.isclass(cls) and cls is not IntegrationCoupling and issubclass(cls, IntegrationCoupling):
        is_integmi = True
    return is_integmi


def sort_integration_couplings_by_precedence(self, coupling_list: List[IntegrationCoupling]) -> List[IntegrationCoupling]:
    """
        Takes a list of :class:`IntegrationCoupling` classes and creates an ordered list based on the ordinal
        precedence declared by the :class:`IntegrationCoupling`.
    """
    precedence_table = {}

    for coupling in coupling_list:
        precedence = coupling.declare_precedence()
        precedence_level_list = None
        if precedence in precedence_table:
            precedence_level_list = precedence_table[precedence]
        else:
            precedence_level_list = []
            precedence_table[precedence] = precedence_level_list
        precedence_level_list.append(coupling)

    precedence_keys_sorted = precedence_table.keys()
    precedence_keys_sorted.sort()

    ordered_couplings = []
    for precedence in precedence_keys_sorted:
        ordered_couplings.extend(precedence_table[precedence])

    return ordered_couplings