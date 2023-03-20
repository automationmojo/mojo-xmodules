
from mojo.xmods.xcollections.mergemap import MergeMap


a = {
    "a": {"a": "a"}
}

b = {
    "a": {
        "a": "aa",
        "b": "bb"
    }
}

mm = MergeMap(a, b)

ma = mm["a"]

av = ma["a"]
bv = ma["b"]

print(f"{av}")

print(f"{bv}")