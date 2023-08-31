"""
.. module:: extensiionproperty
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the `ExtensionProperty` object that is used to extend the functionality of an object
               by adding properties to the object.  The extension property is used to group extension methods so a property
               does not get overloaded.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

from typing import TypeVar

import weakref

OwnerType = TypeVar("OwnerType")

class ExtensionProperty:
    """
        The :class:`ExtensionProperty` object is used to attach extension properties to an owning type.  The extension
        property is used to group extension methods so a property does not get overloaded.
    """

    def __init__(self, owner: OwnerType):
        self._owner_ref = weakref.ref(owner)
        return
    
    def owner(self) -> OwnerType:
        return self._owner_ref()
