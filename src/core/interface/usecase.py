from typing import Any
from abc import ABC, abstractmethod


class UseCase(ABC):
    @abstractmethod
    def execute(self) -> Any | None:
        pass
