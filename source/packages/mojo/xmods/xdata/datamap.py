
"""
.. module:: datamap
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which is contains the :class:`DataMap` object which can be used to
               generate deep dictionary type data objects from a descriptive data map.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""


from typing import Generator

from mojo.errors.exceptions import SemanticError

from mojo.xmods.xdata.datahelpers import insert_into_dict_by_path
from mojo.xmods.xdata.generators.valuegenerator import ValueGenerator


class DataMap:

    map: Dict[str, ValueGenerator] = None

    def __init__(self):
        if self.map is None:
            raise SemanticError("The 'map' class variable must be set on derived classes")
        return

    def traverse_map_for_good_values(self) -> Generator[dict, None, None]:
        
        map = self.map

        for pivot in map.keys():

            other_keys = [k for k in map.keys()]

            nxtval = {}

            for okey in other_keys:
                other_gen = map[okey]

                default = other_gen.default
                insert_into_dict_by_path(okey, default, nxtval)

            pivot_gen = map[pivot]

            pval = pivot_gen.traverse_good()

            insert_into_dict_by_path(pivot, pval, nxtval)

            yield nxtval


    def traverse_map_of_bad_values(self) -> Generator[dict, None, None]:

        map = self.map

        for pivot in map.keys():

            other_keys = [k for k in map.keys()]

            nxtval = {}

            for okey in other_keys:
                other_gen = map[okey]

                default = other_gen.default
                insert_into_dict_by_path(okey, default, nxtval)

            pivot_gen = map[pivot]

            # We only get a bad value for the pivot point
            pval = pivot_gen.traverse_bad()

            insert_into_dict_by_path(pivot, pval, nxtval)

            yield nxtval


if __name__ == "__main__":

    from typing import Any, Dict

    from mojo.xmods.xdata.datanode import DataNode
    from mojo.xmods.xdata.generators.listgenerator import ListGenerator

    good_users = [
        {
            "id": 1000
            "name": "myron"
        }
    ]

    bad_users = [
        {
            "id": -1,
            "name": "myron"
        },
        {
            "id": -1,
            "name": "@myron"
        }
    ]

    class UserGenerator[dict](ListGenerator):
        
        def __init__(self, good=good_users, bad=bad_users):
            return


    class ExampleMap:

        map = {
            "/user": DataNode(UserGenerator())
        }
