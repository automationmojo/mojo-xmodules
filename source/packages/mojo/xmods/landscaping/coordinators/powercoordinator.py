"""
.. module:: powercoordinator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the PowerCoordinator which is used for managing power activity services.

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


from typing import Union, TYPE_CHECKING

from mojo.xmods.exceptions import ConfigurationError
from mojo.xmods.landscaping.coordinators.coordinatorbase import CoordinatorBase
from mojo.xmods.landscaping.agents.poweragentbase import PowerAgentBase

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape

class PowerCoordinator(CoordinatorBase):

    def __init__(self, lscape: "Landscape", *args, **kwargs):
        super(PowerCoordinator, self).__init__(lscape, *args, **kwargs)
        return

    def _initialize(self, *_args, **_kwargs):
        """
            Called by the CoordinatorBase constructor to perform the one time initialization of the coordinator Singleton
            of a given type.
        """
        self._power_config = {}
        for pcfg in self._coord_config:
            cfgname = pcfg["name"]
            self._power_config[cfgname] = pcfg

        self._power_interfaces = {}
        return

    def lookup_agent(self, power_mapping: dict) -> Union[PowerAgentBase, None]:
        """
            Looks up a power agent by power mapping.
        """
        power_agent = None

        pname = power_mapping["name"]
        pswitch = power_mapping["switch"]

        power_iface = self._lookup_power_interface(pname)
        if power_iface is not None:
            power_agent = PowerAgentBase(power_iface, pswitch)
        else:
            errmsg = "Failure to find power interface %r." % pname
            raise ConfigurationError(errmsg) from None

        return power_agent
