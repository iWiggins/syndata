from typing import Any
from abc import ABC, abstractmethod

class RowProcessorBase(ABC):

    @abstractmethod
    def process_row(self, row: list[Any]) -> list[Any]:...