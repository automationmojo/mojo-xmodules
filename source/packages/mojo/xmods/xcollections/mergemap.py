"""
.. module:: mergemap
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`MergeMap` object which is similar to
               a :class:`ChainMap` but which allows shadowed results for descendent
               leaves.

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

from typing import Iterable, List, Optional, MutableMapping

import reprlib

class MergeMap(MutableMapping):

    def __init__(self, *maps: List[MutableMapping]):
        self.maps: List[MutableMapping] = [m for m in maps]
        return

    def clear(self):
        """
            Clears all maps.
        """
        self.maps = []
        return

    def copy(self):
        """
            New MergeMap or subclass with a new copy of maps[0] and refs to maps[1:]
        """
        cpy_maps = [nm.copy() for nm in self.maps]
        nmm = self.__class__(*cpy_maps)
        return nmm

    def get(self, key: str, default=None):
        """
            Gets the value for a key or returns the specified default value.
        """
        rtnval = self[key] if key in self else default
        return rtnval

    def keys(self) -> Iterable[str]:
        """
            Gets the top level possible keys that can be used to query this merge map.
        """

        mks = set()

        for nm in self.maps:
            mks.update(nm.keys())
        
        return mks

    def new_child(self, m: Optional[dict]=None, **kwargs):      # like Django's Context.push()
        """
            New MergeMap with a new map followed by all previous maps.
            If no map is provided, an empty dict is used.
            Keyword arguments update the map or new empty dict.
        """
        if m is None:
            m = kwargs
        elif kwargs:
            m.update(kwargs)
        
        cpy_maps = [nm.copy() for nm in self.maps]

        ncm = self.__class__(m, *cpy_maps)

        return ncm

    def __bool__(self):
        return any(self.maps)

    def __contains__(self, key: str):
        haskey = False
        
        for mapping in self.maps:
            if key in mapping:
                haskey = True
                break

        return haskey

    __copy__ = copy
    
    def __delitem__(self, key):
        kfound = False

        for nm in self.maps:
            if key in nm:
                kfound = True
                del nm[key]
        
        if kfound is not None:
            raise KeyError(f'Key not found in the first mapping: {key!r}')

        return

    def __getitem__(self, key: str):

        merge_val = None

        for mapping in self.maps:
            if key in mapping:
                nm = mapping[key]          # can't use 'key in mapping' with defaultdict
                if merge_val is None:
                    if isinstance(nm, dict):
                        merge_val = MergeMap(nm)
                    else:
                        merge_val = [nm]
                elif isinstance(merge_val, list):
                    merge_val.append(nm)
                else:
                    merge_val.maps.append(nm)

        if merge_val is None:
            self.__missing__(key)  # support subclasses that define __missing__

        if isinstance(merge_val, list):
            merge_val = merge_val[0]

        return merge_val         

    def __iter__(self):
        mks = self.keys()
        return iter(mks)

    def __len__(self):
        """
            Get the length of all possible keys.
        """
        rtnval = len(self.keys())
        return rtnval

    def __missing__(self, key: str):
        raise KeyError(key)

    @reprlib.recursive_repr()
    def __repr__(self):
        rval = f'{self.__class__.__name__}({", ".join(map(repr, self.maps))})'
        return rval

    def flatten(self) -> dict:
        """
            Flattens the Merge dictionary into a flat representation of
            the combined keys and values of the maps.
        """
        fd = {}

        all_keys = self.keys()
        if len(all_keys):
            for k, v in self.items():
                if isinstance(v, MergeMap):
                    v = v.flatten()
                fd[k] = v

        return fd

    @classmethod
    def fromkeys(cls, iterable, *args):
        """
            Create a MergeMap with a single dict created from the iterable.
        """
        nm = cls(dict.fromkeys(iterable, *args))
        return nm

    def __setitem__(self, key, value):
        self.maps[0][key] = value
        return


