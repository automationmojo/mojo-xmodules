
from typing import List, Generator

from mojo.xmods.xdata.generators.valuegenerator import ValueGenerator, VT

class ListGenerator(ValueGenerator[VT]):

    def __init__(self, default: VT, good: List[VT], bad: List[VT]):
        super().__init__(default)
        self._good = good
        self._bad = bad
        return
    
    def traverse_good(self) -> Generator[VT, None, None]:
        for val in self._good:
            yield val
    
    def traverse_bad(self) -> Generator[VT, None, None]:
        for val in self._bad:
            yield val
