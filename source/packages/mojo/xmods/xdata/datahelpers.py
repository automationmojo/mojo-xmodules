

"""
.. module:: datahelpers
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which is fuctions that help to work with collections to generate
               test data.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from typing import Any, Dict, List

def insert_into_dict_by_path(path: str, val: Any, target: Dict[str, Any]):

    path = path.strip()

    path_parts = path.split("/")

    if len(path_parts) == 0:
        raise ValueError(f"Invalid insertion path={path}")

    _recursive_insert_into_dict_by_path(path_parts, val, target)

    return

def _recursive_insert_into_dict_by_path(path_parts: List[str], val: Any, cursor: Dict[str, Any]):

    nxt_part = path_parts.pop()
    
    if len(path_parts) == 0:
        cursor[nxt_part] = val

    else:
        if nxt_part in cursor:
            nxt_cursor = cursor[nxt_part]
            if not isinstance(nxt_cursor, dict):
                nxt_cursor = {}

            _recursive_insert_into_dict_by_path(path_parts, val, nxt_cursor)
        
        else:
            nxt_cursor = {}
            cursor[nxt_part] = nxt_cursor

            _recursive_insert_into_dict_by_path(path_parts, val, nxt_cursor)

    return