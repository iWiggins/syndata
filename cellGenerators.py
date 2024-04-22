from cellgeneratorbase import CellGeneratorBase
from typing import Any, Callable
from random import uniform, choices, randint

class FloatCellGenerator(CellGeneratorBase):
    _low: float
    _high: float
    _round: int
    def __init__(self, low: float, high: float, digits: int):
        self._low = low
        self._high = high
        self._round = digits
    def generate_cell(self, row: int) -> Any:
        return round(uniform(self._low, self._high), self._round)

class StringCellGenerator(CellGeneratorBase):
    _options: list[str]
    _weights: list[float]
    def __init__(self, options: list[str], weights: list[float] | None = None):
        if weights is not None and len(options) != len(weights):
            raise ValueError("number of weights must equal number of choices")
        self._options = options
        self._weights = weights if weights is not None else [1.0]*len(options)
    def generate_cell(self, row: int) -> Any:
        return choices(self._options, self._weights)[0]

class IntCellGenerator(CellGeneratorBase):
    _low: int
    _high: int
    def __init__(self, low: int, high: int):
        self._low = low
        self._high = high
    def generate_cell(self, row: int) -> Any:
        return randint(self._low, self._high)

class CellGenerator(CellGeneratorBase):
    _generator: Callable[[int], Any]
    def __init__(self, generator: Callable[[int], Any]) -> None:
        self._generator = generator
    def generate_cell(self, row: int) -> Any:
        return self._generator(row)