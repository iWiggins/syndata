from abc import ABC, abstractmethod
from typing import Any, Iterable

class PresenterBase(ABC):

    @abstractmethod
    def present(self, headers:list[str], data:Iterable[list[Any]]):...