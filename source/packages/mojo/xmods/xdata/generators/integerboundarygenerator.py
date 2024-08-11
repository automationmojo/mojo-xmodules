
from typing import List, Generator

from mojo.xmods.xdata.generators.valuegenerator import ValueGenerator

class IntegerBoundaryGenerator(ValueGenerator[int]):

    def __init__(self, default: int, max: int, min: int):
        super(int, self).__init__(default)
        self._max = max
        self._min = min
        return
    
    def traverse_good(self) -> Generator[int, None, None]:

        value_list = []

        rangecount = self._max - self._min

        if rangecount == 0:
            value_list = [self._max]
        elif rangecount == 1:
            value_list = [self._max, self._min]
        elif rangecount == 2:
            value_list = [self._max, self._max - 1, self._min]
        elif rangecount >= 3:
            value_list = [self._max, self._max - 1, self._min + 1, self._min]

        for val in value_list:
            yield val
    
    def traverse_bad(self) -> Generator[int, None, None]:

        value_list = [self._max + 1, self._min - 1]

        for val in value_list:
            yield val