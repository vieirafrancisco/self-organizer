from typing import IO
from abc import ABC, abstractmethod


class FileReader(ABC):
    @abstractmethod
    def read(self, file: IO) -> str:
        pass
