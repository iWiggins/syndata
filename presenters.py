from presenterBase import PresenterBase
from typing import Any, Iterable
from csv import writer, QUOTE_STRINGS

class CSVPresenter(PresenterBase):

    _filename: str
    _headers: bool

    def __init__(self, filename: str, showHeaders: bool):
        self._filename = filename
        self._headers = showHeaders

    def present(self, headers: list[str], data: Iterable[list[Any]]):
        with open(self._filename, 'w', newline='') as file:
            write = writer(file, quoting=QUOTE_STRINGS)
            if self._headers:
                write.writerow(headers)
            write.writerows(data)

class TXTPresenter(PresenterBase):

    _filename: str
    _separators: list[str] | str
    _ending: str
    
    def __init__(self, filename: str, separators: list[str] | str, ending: str = "\n"):
        self._filename = filename
        self._separators = separators
        self._ending = ending
    
    def present(self, headers: list[str], data: Iterable[list[Any]]):
        with open(self._filename, 'w') as file:
            iterator = data.__iter__()
            try:
                row = iterator.__next__()
                if isinstance(self._separators, str):
                    seps = [self._separators]*len(row)
                else:
                    seps = self._separators
                for cell in zip(row,seps):
                    file.write(str(cell[0]))
                    file.write(cell[1])
                while True:
                    file.write(self._ending)
                    row = iterator.__next__()
                    for cell in zip(row,seps):
                        file.write(str(cell[0]))
                        file.write(cell[1])
            except StopIteration:
                pass