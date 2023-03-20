"""
.. module:: caseinsensitivestringdict
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`CaseInsensitiveStringDict` object which
               is a case insensitive string keyed dictionary.

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

from typing import Any


class CaseInsensitiveStringDict(dict):
    """
        The :class:`CaseInsensitiveStringDict` is a dictionary that can store and
        recover values associated with a text based key in a case insensative
        way.  It accomplishes this by converting all ascii characters in a key
        to lower case.
    """

    @staticmethod
    def key_to_lower(key: str):
        """
            Converts a key to a lower case string so case insensative comparisons can be made.

            :param key: A key value to check to see if an object is stored under the key.
        """
        if not isinstance(key, str):
            raise KeyError("Only string keys can be used with the CaseInsensitiveStringDict type.")

        key = key.lower()
        return key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveStringDict, self).__init__(*args, **kwargs)
        self._convert_keys()
        return

    def __contains__(self, key: str) -> bool:
        """
            Overrides the :method:`__contains__` operator providing a key conversion in order
            to perform a case insensative dictionary key lookup.

            :param key: A key value to check to see if an object is stored under the key.

            :returns: A boolean indicating if the key provided is in this objects keys.
        """
        return super(CaseInsensitiveStringDict, self).__contains__(CaseInsensitiveStringDict.key_to_lower(key))

    def __delitem__(self, key: str):
        """
            Overrides the :method:`__delitem__` operator providing a key conversion in order
            to perform a case insensative dictionary item delete.

            :param key: A key value to delete the object stored under the key.

            :raises: KeyError
        """
        return super(CaseInsensitiveStringDict, self).__delitem__(CaseInsensitiveStringDict.key_to_lower(key))

    def __getitem__(self, key: str) -> Any:
        """
            Overrides the :method:`__getitem__` operator providing a key conversion in order
            to perform a case insensative dictionary item lookup.

            :param key: A key value to lookup and return the object stored under the key.

            :returns: The object associated with the key provided.

            :raises: KeyError
        """
        return super(CaseInsensitiveStringDict, self).__getitem__(CaseInsensitiveStringDict.key_to_lower(key))

    def __setitem__(self, key: str, value: Any):
        """
            Overrides the :method:`__setitem__` operator providing a key conversion in order
            to perform a case insensative dictionary item set.

            :param key: A key value to use to store the object stored under the key.
            :param value: The value to store with the key.
        """
        super(CaseInsensitiveStringDict, self).__setitem__(CaseInsensitiveStringDict.key_to_lower(key), value)

    def pop(self, key: str, *args, **kwargs) -> Any:
        """
            Overrides the :method:`pop` method providing a key conversion in order
            to perform a case insensative dictionary pop item.

            :param key: A key value to use to pop and return the object stored under the key.

            :returns: The object associated with the key provided.

            :raises: KeyError
        """
        return super(CaseInsensitiveStringDict, self).pop(CaseInsensitiveStringDict.key_to_lower(key), *args, **kwargs)

    def get(self, key: str, *args, **kwargs) -> Any:
        """
            Overrides the :method:`get` method providing a key conversion in order
            to perform a case insensative dictionary get item.

            :param key: A key value to use to get and return the object stored under the key.

            :returns: The object associated with the key provided.

            :raises: KeyError
        """
        return super(CaseInsensitiveStringDict, self).get(CaseInsensitiveStringDict.key_to_lower(key), *args, **kwargs)

    def setdefault(self, key: str, value: Any, *args, **kwargs):
        """
            Overrides the :method:`setdefault` method providing a key conversion in order
            to perform a case insensative dictionary setdefault for the given key.

            :param key: A key value to use to store the object stored under the key.
            :param value: The default value to store with the key.
        """
        return super(CaseInsensitiveStringDict, self).setdefault(CaseInsensitiveStringDict.key_to_lower(key), value, *args, **kwargs)

    def update(self, dobj: dict = {}, **kwargs): # pylint: disable=dangerous-default-value
        """
            Overrides the :method:`update` method providing a key conversion in order
            to perform a case insensative dictionary update.
        """
        super(CaseInsensitiveStringDict, self).update(self.__class__(dobj))
        super(CaseInsensitiveStringDict, self).update(self.__class__(**kwargs))
        return

    def _convert_keys(self):
        """
            Used by the :class:`CaseInsensitiveStringDict` constructor to convert the keys of
            initialization dictionaries to lower case keys so we can perform case insensative
            key lookups.
        """
        for key in list(self.keys()):
            val = super(CaseInsensitiveStringDict, self).pop(key)
            self.__setitem__(key, val)
        return
