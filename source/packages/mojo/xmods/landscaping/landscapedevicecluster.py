"""
.. module:: landscapedevicecluster
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module contains the :class:`LandscapeDeviceCluster` object which 
               represents a cluster of devices that are compute nodes in a
               computer or storage cluster.

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

from typing import List

from mojo.xmods.landscaping.cluster.nodebase import NodeBase
from mojo.xmods.landscaping.landscapedevicecluster import LandscapeDeviceCluster
class LandscapeDeviceCluster:
    """
        A :class:`LandscapeDeviceGroup` object is used to group devices to an associated
        grouping label.
    """

    def __init__(self, label: str, nodes: List[NodeBase], group: LandscapeDeviceGroup) -> None:
        self._label = label
        self._nodes = nodes
        self._group = group
        return

    @property
    def group(self):
        return self._group

    @property
    def label(self):
        return self._label

    @property
    def nodes(self):
        return self._nodes
