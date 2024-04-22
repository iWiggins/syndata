from typing import Any

class StringBuilder:

    _data: list[str]

    def __init__(self):
        self._data = []
    
    def __str__(self):
        return ''.join(self._data)
    
    def append(self, object: Any):
        self._data.append(str(object))
    
    def append_line(self, object: Any = None):
        if object is not None:
            self._data.append(str(object))
        self._data.append('\n')