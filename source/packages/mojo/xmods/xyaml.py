
from typing import List

import yaml

from mojo.xmods.xcollections.mergemap import MergeMap


def safe_load_yaml_files_as_mergemap(filenames: List[str]) -> MergeMap:
    """
        Creates a :class:`MergeMap` from a list of yaml configuration files.
    """
    merge_map = MergeMap()

    for fname in filenames:
        with open(fname, 'r') as lf:
            lfcontent = lf.read()
            finfo = yaml.safe_load(lfcontent)

            merge_map.maps.insert(0, finfo)

    return merge_map
