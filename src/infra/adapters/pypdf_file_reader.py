from typing import IO

import PyPDF2

from core.interface import FileReader


class PyPDFFileReader(FileReader):
    def read(self, file: IO) -> str:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
