import PyPDF2
import google.generativeai as genai
from nltk.tokenize import word_tokenize

from .settings import GOOGLE_API_KEY


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
