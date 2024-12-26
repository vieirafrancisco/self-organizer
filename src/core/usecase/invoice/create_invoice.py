from datetime import date
from uuid import uuid4

from src.core.entity import Invoice
from src.core.interface.usecase import UseCase


class CreateInvoiceUseCase(UseCase):
    def __init__(self, due_date: date, bank_name: str):
        self.due_date = due_date
        self.bank_name = bank_name

    def execute(self):
        invoice = Invoice(
            id=uuid4(), due_date=self.due_date, bank_name=self.bank_name
        )

        return invoice
