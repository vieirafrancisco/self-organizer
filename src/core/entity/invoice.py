from typing import List
from datetime import date


class Invoice:
    def __init__(
        self,
        id: str,
        due_date: date,
        bank_name: str,
        file_raw_text: str = '',
        file_prep_data: List[dict] | None = None,
    ):
        self.id = id
        self.due_date = due_date
        self.bank_name = bank_name
        self.file_raw_text = file_raw_text
        self.file_prep_data = file_prep_data or []
