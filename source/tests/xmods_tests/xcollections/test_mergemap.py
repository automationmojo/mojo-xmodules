
import unittest

from mojo.xmods.xcollections.mergemap import MergeMap

class TestMergeMap(unittest.TestCase):

    map_zero = {
        "a": {
            "a": "a"
        }
    }

    map_one = {
        "a": {
            "a": {
                "a": "aa",
                "z": "zz"
            },
            "b" : {
                "b": "bb",
                "c": "cc"
            }
        }
    }

    map_two = {
        "a": {
            "a": {
                "a": "aa",
                "z": "zz"
            },
            "e" : {
                "c": "aa",
                "d": "dd"
            }
        },
        "e": {
            "f": {
                "g": "gg",
                "h": "hh"
            }
        }
    }

    def test_map_shadows_value(self):

        mm = MergeMap(self.map_two, self.map_one, self.map_zero)

        ma = mm["a"]
        maa = ma["a"]

        self.assert_(isinstance(maa, MergeMap), "The map_two value should be the priority value.")
        return
    
    def test_value_shadows_map(self):

        mm = MergeMap(self.map_zero, self.map_one, self.map_two)
        ma = mm["a"]["a"]

        self.assert_(ma == "a", "The map_zero value should be the priority value.")
        return

if __name__ == '__main__':
    unittest.main()
