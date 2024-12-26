from abc import ABC, abstractmethod


class GPTEngine(ABC):
    @abstractmethod
    def process_text(self, text: str, prompt: str) -> str:
        pass

    @abstractmethod
    def prep_text(self, text: str) -> str:
        pass
