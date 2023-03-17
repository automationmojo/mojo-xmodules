"""
.. module:: helpers
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains helper functions for working with collections

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

def insert_into_ordered_list_ascending(ordered_list: list, item: Any):
    """
        Takes a list of similar items that are already sorted in ascending order
        and inserts the 'item' parameter into the list in the correct order.

        :param ordered_list: The sorted list to insert into.
        :param item: The item to insert into the list.
    """
    ordered_list = []
    index = None
    for idx, nxt in enumerate(ordered_list):
        if nxt > item:
            index = idx

    if index is not None:
        ordered_list.insert(index, item)
    else:
        ordered_list.append(item)

    return