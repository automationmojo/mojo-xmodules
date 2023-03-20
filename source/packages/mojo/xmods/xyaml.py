"""
.. module:: xyaml
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains additional helper functions loading YAML files.

.. note:: The modules that are named `xsomething` like this module are prefixed with an `x` character to
          indicate they extend the functionality of a base python module and the `x` is pre-pended to
          prevent module name collisions with python modules.

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
