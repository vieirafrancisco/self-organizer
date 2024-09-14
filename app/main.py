from flask import Blueprint, render_template, request

from .services import (
    extract_text_from_pdf,
    process_text_with_gemini,
    serialize_text,
)

main = Blueprint('main', __name__)


@main.route('/')
def init():
    return render_template('index.html')


@main.route('/', methods=['POST'])
def upload_pdf():
    pdf_file = request.files['pdf']
    text = extract_text_from_pdf(pdf_file)
    summary = process_text_with_gemini(text)
    return render_template('index.html', debts=serialize_text(summary.text))
