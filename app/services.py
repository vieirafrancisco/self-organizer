import PyPDF2
import google.generativeai as genai
from nltk.tokenize import word_tokenize
from sqlalchemy.exc import SQLAlchemyError

from .settings import GOOGLE_API_KEY
from .models import Debt, Invoice, db


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
        'Date in format YYYY-MM-DD, if year not present then '
        'current year.'
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


def build_debts(invoice_id: int, debts: list[dict]):
    """Gera instâncias do modelo Debt."""
    for debt_args in debts:
        yield Debt(invoice_id=invoice_id, **debt_args)


def save_invoice_with_debts(
    bank_name: str, ref_date: str, file_raw_text: str, debts: list[dict]
):
    """Salva uma fatura (Invoice) e suas dívidas (Debts) no banco de dados."""
    invoice = Invoice(
        bank_name=bank_name,
        ref_date=ref_date,
        file_raw_text=file_raw_text,
    )

    try:
        # Usando uma transação atômica
        db.session.add(invoice)
        db.session.flush()  # Obtém o `id` da fatura sem fazer `commit`

        # Adiciona as dívidas relacionadas
        db.session.add_all(build_debts(invoice.id, debts))

        db.session.commit()

        return invoice  # Retorna o objeto criado, se necessário
    except SQLAlchemyError as e:
        db.session.rollback()  # Reverte todas as operações em caso de erro
        raise RuntimeError(f'Erro ao salvar fatura e dívidas: {e}')
