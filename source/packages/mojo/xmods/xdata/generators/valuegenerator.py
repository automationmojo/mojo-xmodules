
"""
.. module:: valuegenerator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which is contains the :class:`ValueGenerator` object which serves as
               a base class for value generator objects.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""


from typing import TypeVar, Generic, Generator

VT = TypeVar("VT")

class ValueGenerator(Generic[VT]):
    """
    """

    def __init__(self, default: VT):
        self._default = default
        return
    
    @property
    def default(self) -> VT:
        return self._default
    
    def traverse_field_of_good_values(self) -> Generator[VT, None, None]:
        raise StopIteration
    
    def traverse_field_of_bad_values(self) -> Generator[VT, None, None]:
        raise StopIteration
