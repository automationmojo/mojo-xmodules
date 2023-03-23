"""
.. module:: xpython
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains additional helper functions for modifying the root
               python behavior

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

import os
import sys

def extend_path(dir_to_add: str) -> None:
    """
        Extends the PYTHONPATH in the current python process and also modifies
        'PYTHONPATH' so the child processes will also see inherit the extension
        of 'PYTHONPATH'.
    """
    found = False

    for nxt_item in sys.path:
        nxt_item = nxt_item.rstrip(os.sep)
        dir_to_add = dir_to_add.rstrip(os.sep)
        if nxt_item == dir_to_add:
            found = True
            break

    if not found:
        sys.path.insert(0, dir_to_add)
        if "PYTHONPATH" in os.environ:
            os.environ["PYTHONPATH"] = dir_to_add + os.pathsep + os.environ["PYTHONPATH"]
        else:
            os.environ["PYTHONPATH"] = dir_to_add

    return
