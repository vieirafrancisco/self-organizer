from unittest import TestCase
from datetime import date

from src.core.entity import Invoice
from src.core.usecase.invoice.read_file import ReadFileUseCase
from src.infra.adapters.mock import FakeGPTEngine, FakeFileReader


class TestReadFileUseCase(TestCase):
    def setUp(self):
        self.invoice = Invoice('id', date(2024, 12, 25), 'nubank')
        self.file_reader = FakeFileReader()
        self.gpt_engine = FakeGPTEngine()

        return super().setUp()

    def test_read_file_flow(self):
        read_file = ReadFileUseCase(
            self.invoice, 'fake_path', self.file_reader, self.gpt_engine
        )

        raw_text = read_file._read_file('fake_path')
        self.assertEqual(raw_text, 'fake result')

        prep_data = read_file._prep_data(raw_text)
        self.assertEqual(
            prep_data[0],
            {
                'date': '0',
                'description': '0',
                'amount': float(0),
                'total_installments': int(0),
                'paid_installments': int(0),
            },
        )
