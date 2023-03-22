"""
.. module:: configured
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing functions and classes that help create and work with
               configuration based extension objects.

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

from typing import List, Type

from typing import Callable, Generator, List, Union, Type

from mojo.xmods.ximport import import_by_name

import inspect
import logging

logger = logging.getLogger()

class ExtensionPointsFactory:
    """
        The base class used to extend
    """

def is_subclass_of_extension_points_factory(cand_type):
    """
        Returns a boolean value indicating if the candidate type is a subclass
        of :class:`Landscape`.
    """
    is_scoep = False
    if inspect.isclass(cand_type):
        if cand_type != ExtensionPointsFactory and issubclass(cand_type, ExtensionPointsFactory):
            is_scoep = True
    return is_scoep


def load_and_set_extension_points_factory_type(module_name: str):
    """
        Scans the module provided for :class:`Landscape` derived classes and will
        take the first one and assign it as the current runtime landscape type.
    """
    factory_type = None

    extpt_module = import_by_name(module_name)
    class_items = inspect.getmembers(extpt_module, is_subclass_of_extension_points_factory)

    extension_classes = []
    for _, cls_type in class_items:
        type_module_name = cls_type.__module__
        if type_module_name == extpt_module.__name__:
            extension_classes.append(cls_type)

    if len(extension_classes) > 1:
        wmsg = f"Only one ExtensionPoints class is allowed per module in order to perserve ordering. module={extpt_module}"
        logger.warning(wmsg)

    if len(extension_classes) > 0:
        factory_type = extension_classes[0]
    else:
        wmsg = f"Found extension module={extpt_module} without an `ExtensionPoints` derived class."
        logger.warning(wmsg)

    return factory_type


class SuperFactory:
    """
        A :class:`SuperFactory` object is used to maintain a chain of factory types that
        can be traversed in order to locate a factory the implements a specific protocol
        in order to enable various types of overload or overinstance states.
    """

    search_modules = [
        'mojo.xmods.landscaping.extensionpoints'
    ]

    extension_factories = []

    def __init__(self):

        self.extension_factories.clear()

        for smod in self.search_modules:
            factory_type = load_and_set_extension_points_factory_type(smod)
            if factory_type is not None:
                self.extension_factories.append(factory_type)

        return

    def create_instance_by_order(self, factory_method: Union[str, Callable], *args, **kwargs) -> Union[object, None]:

        instance = None

        create_instance: Callable = None

        if not isinstance(factory_method, str):
            factory_method = factory_method.__name__

        for factory_type in self._extension_factories:
            if hasattr(factory_type, factory_method):
                create_instance = getattr(factory_type, factory_method)
        
        if create_instance is not None:
            instance = create_instance(factory_type, *args, **kwargs)

        return instance

    def create_instance_for_each(self, factory_method: Union[str, Callable], *args, **kwargs):

        instance_list = []

        if not isinstance(factory_method, str):
            factory_method = factory_method.__name__

        for factory_type in self._extension_factories:
            if hasattr(factory_type, factory_method):
                create_instance = getattr(factory_type, factory_method)
                instance_list.append(create_instance)

        return instance_list

    def get_override_types_by_order(self, get_type_method: Union[str, Callable]) -> Union[Type, List[Type], None]:

        found_type = None

        get_type_with = None

        if not isinstance(get_type_method, str):
            get_type_method = get_type_method.__name__
        
        for factory_type in self.extension_factories:
            if hasattr(factory_type, get_type_method):
                get_type_with = getattr(factory_type, get_type_method)
        
        if get_type_with is not None:
            found_type = get_type_with()
        
        return found_type
    
    def interate_override_types_for_each(self, get_type_method: Union[str, Callable]) -> Generator[Union[Type, List[Type], None], None, None]:

        found_type = None

        get_type_with = None

        if not isinstance(get_type_method, str):
            get_type_method = get_type_method.__name__
        
        for factory_type in self.extension_factories:
            if hasattr(factory_type, get_type_method):
                get_type_with = getattr(factory_type, get_type_method)
        
                found_type = get_type_with()
                yield found_type
