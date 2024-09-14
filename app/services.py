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
    # Tokenização
    tokens = word_tokenize(text)

    # Junta os tokens novamente em uma string para passar para o Gemini
    # (Você pode personalizar essa junção para suas necessidades)
    processed_text = ' '.join(tokens)

    # Configura a sua chave API do Gemini
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.0-pro-latest')

    # Exemplo: Resumir o texto
    prompt = (
        f'No texto "{processed_text}", retorne no formato csv '
        'todas as transações seguindo a regra: '
        'data, descrição, valor, parcela atual, total parcelas. '
        'O valor precisa ser somente digitos '
        'com o divisor decimal ".". '
        'Quando na descrição tiver o padrão x/y, em que x e y são digitos,'
        'separe os digitos x e y da "/" e '
        'posicione o digito x na coluna "parcela atual" '
        'e o digito y na coluna "total parcelas". '
        'Caso não tenha esse padrão posicione ambas com valor 1.'
    )
    response = model.generate_content(prompt)
    return response


def serialize_text(text):
    rows = text.split('\n')
    for row in rows:
        fields = row.split(',')
        yield {
            'date': fields[0],
            'description': fields[1],
            'amount': float(fields[2]),
            'total_installments': int(fields[3]),
            'paid_installments': int(fields[4])
        }
