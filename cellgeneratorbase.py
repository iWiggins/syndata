from typing import Any
from abc import ABC, abstractmethod

class CellGeneratorBase(ABC):

    @abstractmethod
    def generate_cell(self, row: int) -> Any:...