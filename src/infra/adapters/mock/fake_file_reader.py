from src.core.interface import FileReader


class FakeFileReader(FileReader):
    def read(self, file):
        return 'fake result'
