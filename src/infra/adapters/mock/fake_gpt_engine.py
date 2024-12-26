from src.core.interface import GPTEngine


class FakeGPTEngine(GPTEngine):
    def process_text(self, text, prompt):
        return '0,0,0,0,0\n1,1,1,1,1\n2,2,2,2,2'
