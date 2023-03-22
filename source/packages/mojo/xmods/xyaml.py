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

import logging
import os

import yaml

from mojo.xmods.exceptions import ConfigurationError
from mojo.xmods.xcollections.mergemap import MergeMap


logger = logging.getLogger()

def safe_load_yaml_files_as_mergemap(filenames: List[str], context: str=None) -> MergeMap:
    """
        Creates a :class:`MergeMap` from a list of yaml configuration files.
    """
    merge_map = MergeMap()

    for fname in filenames:
        if os.path.exists(fname):
            with open(fname, 'r') as lf:
                lfcontent = lf.read()
                finfo = yaml.safe_load(lfcontent)

                merge_map.maps.insert(0, finfo)
        else:
            errmsg = f"File not found. '{fname}'"
            if context is not None:
                logger.warn(f"{context} file not found. '{fname}'")
            raise ConfigurationError(errmsg)

    return merge_map
