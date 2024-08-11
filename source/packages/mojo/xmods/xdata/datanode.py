"""
.. module:: datanode
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which is contains the :class:`DataNode` object which acts as a container
               which identifies value generation type and parameters for a node in a value
               map for given point in a result value tree.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from typing import Any, List, Generic, Generator

from mojo.xmods.xdata.generators.valuegenerator import ValueGenerator, VT


class DataNode(Generic[VT]):

    def __init__(self, generator: ValueGenerator[VT], required: bool, dependencies: List[str] = []):
        self._generator = generator
        self._required = required
        self._dependencies = dependencies
        return
    
    @property
    def default(self) -> VT:
        return self._generator.default

    @property
    def dependencies(self) -> List[str]:
        return self._dependencies

    @property
    def generator(self) -> ValueGenerator:
        return self._generator

    @property
    def required(self) -> bool:
        return self._required
    
    def traverse_field_for_good_values(self) -> Generator[VT, None, None]:
        for val in self._generator.traverse_field_of_good_values():
            yield val
    
    def traverse_field_for_bad_values(self) -> Generator[VT, None, None]:
        for val in self._generator.traverse_field_of_bad_values():
            yield val