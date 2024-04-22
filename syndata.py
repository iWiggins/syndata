from cellgeneratorbase import CellGeneratorBase
from presenterBase import PresenterBase
from presenters import CSVPresenter, TXTPresenter
from cellGenerators import CellGenerator, FloatCellGenerator, IntCellGenerator, StringCellGenerator, IndexCellGenerator
from rowprocessorbase import RowProcessorBase
from rowprocessors import CellCorruptionProcessor, CellNullProcessor
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

    def addIndex(self, header: str) -> Self:
        self._headers.append(header)
        self._cells.append(IndexCellGenerator())
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
    
    def dump(self, presenter: PresenterBase, count: int) -> Self:
        data = self.generate(count)
        presenter.present(self._headers, data)
        return self
    
    def dumpCSV(self, filename: str, count: int, showHeaders: bool = True) -> Self:
        CSVPresenter(filename, showHeaders).present(self._headers, self.generate(count))
        return self

    def dumpTXT(self, filename: str, count: int, separators: list[str] | str, ending: str = '\n') -> Self:
        TXTPresenter(filename, separators, ending).present(self._headers, self.generate(count))
        return self