from typing import Any
from rowprocessorbase import RowProcessorBase
from random import random, randint, uniform, choice
from string import ascii_lowercase, ascii_uppercase, digits

all_chars = ascii_uppercase + ascii_lowercase + digits

def random_char() -> str:
    return choice(all_chars)

class CellCorruptionProcessor(RowProcessorBase):
    
    _chances: list[float]
    _intmul: int
    _floatmul: int
    _charmut: float

    def __init__(self, chances: list[float], intmul: int = 3, floatmul: int = 3, charmut: float = 0.5):
        self._chances = chances
        self._intmul = intmul
        self._floatmul = floatmul
        self._charmut = charmut
    
    def process_row(self, row: list[Any]) -> list[Any]:
        if len(row) != len(self._chances):
            raise ValueError("row length does not equal chances length")
        result: list[Any] = []
        for cell in zip(self._chances, row):
            result.append(self._corrupt(cell[0], cell[1]))
        return result
    
    def _corrupt(self, chance: float, item: Any) -> Any:
        if isinstance(item, int):
            return self._corrupt_int(chance, item)
        elif isinstance(item, float):
            return self._corrupt_float(chance, item)
        elif isinstance(item, str):
            return self._corrupt_string(chance, item)
        else:
            return self._corrupt_any(chance, item)

    def _corrupt_int(self, chance: float, item: int) -> int:
        if random() < chance:
            mutator = randint(0, item*self._intmul)
            return item + mutator if random() > 0.5 else item - mutator
        else:
            return item

    def _corrupt_float(self, chance: float, item: float) -> float:
        if random() < chance:
            mutator = uniform(0, item*self._floatmul)
            return item + mutator if random() > 0.5 else item - mutator
        else:
            return item

    def _corrupt_string(self, chance: float, item: str) -> str:
        if random() < chance:
            chars: list[str] = []
            for c in item:
                if random() < self._charmut:
                    chars.append(random_char())
                else:
                    chars.append(c)
            return ''.join(chars)
        else:
            return item

    def _corrupt_any(self, chance: float, item: Any) -> str:
        return "" if random() < chance else item

class CellNullProcessor(RowProcessorBase):

    _chances: list[float]

    def __init__(self, chances: list[float]):
        self._chances = chances
    
    def process_row(self, row: list[Any]) -> list[Any]:
        if len(self._chances) != len(row):
            raise ValueError("row length does not equal chances length")
        results: list[Any] = []
        for cell in zip(self._chances, row):
            if random() < cell[0]:
                results.append("")
            else:
                results.append(cell[1])
        return results