
from typing import Dict, List, Any, Optional, Union, Iterable

import re

from collections import ChainMap

from mojo.collections.mergemap import MergeMap

REGEX_PATH_VALIDATOR = re.compile("/{1}([-a-zA-Z0-9_]+)")

def validate_path_name(path: str) -> List[str]:
    """
        Validates a context pathname.

        :param path: The path to validate and determine its parts.

        :returns: The seperate parts of the path provided.
    """

    parts = None
    mobj = REGEX_PATH_VALIDATOR.findall(path)
    if mobj is not None:
        parts = list(mobj)

    return parts


class DictFsCursor:

    def __init__(self, path: str, store: Dict[str, Any]):
        self._path = path
        self._store = store
        return
    
    def lookup(self, path: Union[str, Iterable[str]], default: Optional[Any]=None, raise_error: bool=True) -> Union["DictFsCursor", Iterable[Any], Any]:
        """
            Lookup an object at the path specified.

            :param path: Path where the desired object is located.

            :returns: The object stored at the specified path.

            :raises: :class:`LookupError`
        """
        found = None

        try:
            if isinstance(path, (list, tuple)):
                path_parts = path
                path = "/%s" %  "/".join(path_parts)
            else:
                path_parts = validate_path_name(path.rstrip("/"))

            found = self._lookup(path=path, sloc=[], sref=self._store, path_parts=path_parts, default=default)
        except LookupError:
            if raise_error:
                raise

        return found
    
    def remove(self, path: str) -> Any:
        """
            Remove an object at the specified path

            :param path: Path where the desired object is located.

            :returns: The being removed from the specified path.

            :raises: :class:`LookupError`
        """
        found_node = None

        if isinstance(path, (list, tuple)):
            path_parts = path
            path = "/%s" %  "/".join(path_parts)
        else:
            path_parts = validate_path_name(path.rstrip("/"))

        found_node = self._remove(path=path, sref=self._store, path_parts=path_parts)

        return found_node

    def insert(self, path: str, obj: Any):
        """
            Insert an object at the path specified.

            :param path: Path where the object is to be inserted
            :param obj: The object to insert

            :raises: :class:`ValueError`
        """
        if isinstance(path, (list, tuple)):
            path_parts = path
            path = "/%s" %  "/".join(path_parts)
        else:
            path_parts = validate_path_name(path.rstrip("/"))

        self._insert(path=path, sref=self._store, path_parts=path_parts, obj=obj)

        return

    def _lookup(self, *, path: str, sloc: List[str], sref: dict, path_parts: List[str], default: Optional[Any]=None) -> Any:

        found = None

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if leaf_name in sref:
                found = sref[leaf_name]
                if len(path_parts) > 1:
                    if isinstance(found, (dict, ChainMap, MergeMap)):
                        floc = sloc + path_parts[:1] 
                        found = self._lookup(path=path, sloc=floc, sref=found, path_parts=path_parts[1:], default=default)
                    else:
                        raise LookupError("Context lookup failure for path=%s" % path)
                else:
                    if isinstance(found, (dict, ChainMap, MergeMap)):
                        cpath = "/" + "/".join(path_parts)
                        found = DictFsCursor(cpath, found)
            elif default is not None:
                if len(path_parts) > 1:
                    found = {}
                    sref[leaf_name] = found
                    floc = sloc + path_parts[:1]
                    found = self._lookup(path=path, sloc=floc, sref=found, path_parts=path_parts[1:], default=default)
                else:
                    sref[leaf_name] = default
                    if isinstance(default, dict):
                        cpath = "/" + "/".join(path_parts)
                        found = DictFsCursor(cpath, default)
                    else:
                        found = default
            else:
                raise LookupError("Context lookup failure for path=%s" % path)
        else:
            raise ValueError("Invalid path=%s" % path)

        return found

    def _remove(self, *, path: str, sref: dict,  path_parts: List[str]) -> Any:

        found = None

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if leaf_name in sref:
                found = sref[leaf_name]
                if len(path_parts) > 1:
                    if isinstance(found, (dict, ChainMap, MergeMap)):
                        found = self._remove(path=path, sref=found, path_parts=path_parts[1:])
                    else:
                        raise LookupError("Context remove failure for path=%s" % path)
                else:
                    del sref[leaf_name]
            else:
                raise LookupError("Context remove failure for path=%s" % path)
        else:
            raise ValueError("Invalid path=%s" % path)

        return found
    
    def _insert(self, *, path: str, sref: dict, path_parts: List[str], obj: Any) -> Any:

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if len(path_parts) > 1:
                if leaf_name not in sref:
                    sref[leaf_name] = {}
                found = sref[leaf_name]
                self._insert(path=path, sref=found, path_parts=path_parts[1:], obj=obj)
            else:
                sref[leaf_name] = obj
        else:
            raise ValueError("Invalid path=%s" % path)

        return

class DictFs(DictFsCursor):

    def __init__(self, root: Dict[str, Any]) -> None:
        super().__init__("/", root)
        return
    

if __name__ == "__main__":
    
    testdict = {
        "a": { "a" : 1 },
        "b": 2,
        "c": { "a": { "a": 1, "b": 2}}
    }

    dfs = DictFs(testdict)

    print(dfs.lookup("/a/a"))
    print(dfs.lookup("/c/a/b"))

    cc = dfs.lookup("/c")
    print(cc.lookup("/a/b"))
