from cellgeneratorbase import CellGeneratorBase
from cellGenerators import CellGenerator, FloatCellGenerator, IntCellGenerator, StringCellGenerator
from rowprocessorbase import RowProcessorBase
from rowprocessors import CellCorruptionProcessor, CellNullProcessor
from csv import writer
from csv import QUOTE_STRINGS
from typing import Self, Generator, Any, Callable

class SynDataGenerator:
    _headers: list[str]
    _cells: list[CellGeneratorBase]
    _processors: list[RowProcessorBase]

    def __init__(self):
        self._headers = []
        self._cells = []
        self._processors = []
    
    def addCell(self, header: str, generator: CellGeneratorBase) -> Self:
        self._headers.append(header)
        self._cells.append(generator)
        return self
    
    def addFloat(self, header: str, min: float, max: float, digits: int) -> Self:
        self._headers.append(header)
        self._cells.append(FloatCellGenerator(min, max, digits))
        return self
    
    def addInt(self, header: str, min: int, max: int) -> Self:
        self._headers.append(header)
        self._cells.append(IntCellGenerator(min, max))
        return self
    
    def addString(self, header: str, choices: list[str], weights: list[float] | None = None) -> Self:
        self._headers.append(header)
        self._cells.append(StringCellGenerator(choices, weights))
        return self
    
    def addFunction(self, header: str, generator: Callable[[int], Any]) -> Self:
        self._headers.append(header)
        self._cells.append(CellGenerator(generator))
        return self

    def addProcessor(self, processor: RowProcessorBase) -> Self:
        self._processors.append(processor)
        return self
    
    def addBlankCells(self, chances: list[float]) -> Self:
        if len(chances) != len(self._cells):
            raise ValueError("row length does not equal chances length")
        self._processors.append(CellNullProcessor(chances))
        return self
    
    def addCorruptCells(self, chances: list[float], intmul: int = 3, floatmul: int = 3, charmut: float = 0.5) -> Self:
        if len(chances) != len(self._cells):
            raise ValueError("row length does not equal chances length")
        self._processors.append(CellCorruptionProcessor(chances, intmul, floatmul, charmut))
        return self
    
    def generate(self, count: int) -> Generator[Any, Any, None]:
        for i in range(0, count):
            row = [gen.generate_cell(i) for gen in self._cells]
            for processor in self._processors:
                row = processor.process_row(row)
            yield row
    
    def dump(self, filename: str, count: int):
        with open(filename, 'w', newline='') as file:
            write = writer(file, quoting=QUOTE_STRINGS)
            write.writerow(self._headers)
            write.writerows(self.generate(count))