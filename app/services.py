from datetime import date

import PyPDF2
import google.generativeai as genai
from nltk.tokenize import word_tokenize

from .settings import GOOGLE_API_KEY
from .models import Debt, Invoice


def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text


def process_text_with_gemini(text):
    tokens = word_tokenize(text)
    processed_text = ' '.join(tokens)

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = (
        f'From the following text "{processed_text}", '
        'extract all transactions as a list of JSON objects with the fields: '
        'date, description, value, paid_installment, total_installments. '
        'Ensure "value" is a numeric string with a decimal point. '
        'If the description contains a pattern "x/y" '
        '(where both x and y are digits), assign "x" to "paid_installment" '
        'and "y" to "total_installments". '
        'If the pattern is not present, set both "paid_installment" '
        'and "total_installments" to 1.'
    )
    response = model.generate_content(prompt)
    return response


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


def save_invoice_to_db(
    bank_name: str, ref_date: date, debts: list, file_raw_text: str
) -> Invoice:
    def build_debts():
        for debt in debts:
            yield Debt(**debt)

    return Invoice(
        bank_name=bank_name,
        ref_date=ref_date,
        debts=list(build_debts()),
        file_raw_text=file_raw_text,
    ).save()
