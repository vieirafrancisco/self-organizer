from typing import List

from src.core.usecase import UseCase
from src.core.entity import Invoice
from src.core.interface import FileReader, GPTEngine


class ReadFileUseCase(UseCase):
    def __init__(
        self,
        invoice: Invoice,
        file_path: str,
        file_reader: FileReader,
        gpt_engine: GPTEngine,
    ):
        self.invoice = invoice
        self.file_path = file_path
        self.file_reader = file_reader
        self.gpt_engine = gpt_engine

    def _read_file(self, file_path: str) -> str:
        with open(file_path, 'w') as f:
            raw_text = self.file_reader.read(f)
        return raw_text

    def _prep_data(self, raw_text: str) -> List[dict]:
        def prep_text(text):
            return text.replace('\n', '').replace('`', '').replace('json', '')

        def serialize_text(text):
            rows = text.split('\n')
            for row in rows:
                fields = row.split(',')
                yield {
                    'date': fields[0],
                    'description': fields[1],
                    'amount': float(fields[2]),
                    'total_installments': int(fields[3]),
                    'paid_installments': int(fields[4]),
                }

        prompt = (
            'From the following text %s, '
            'extract all transactions as a '
            'list of JSON objects with the fields: '
            'date, description, value, paid_installment, total_installments. '
            'Ensure "value" is a numeric string with a decimal point. '
            'If the description contains a pattern "x/y" '
            '(where both x and y are digits), '
            'assign "x" to "paid_installment" '
            'and "y" to "total_installments". '
            'If the pattern is not present, set both "paid_installment" '
            'and "total_installments" to 1.'
            'Date in format YYYY-MM-DD, if year not present then '
            'current year.'
        )

        gpt_text = self.gpt_engine.process_text(raw_text, prompt)
        preped_text = prep_text(gpt_text)
        serialized_text = serialize_text(preped_text)

        return list(serialized_text)

    def execute(self):
        file_raw_text = self._read_file(self.file_path)
        file_prep_data = self._prep_data(file_raw_text)

        self.invoice.file_raw_text = file_raw_text
        self.invoice.file_prep_data = file_prep_data
