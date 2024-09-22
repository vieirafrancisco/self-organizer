import json
from flask import Blueprint, render_template, request, redirect, url_for

from .services import (
    extract_text_from_pdf,
    process_text_with_gemini,
    prep_text,
    save_invoice_to_db,
)
from .models import Invoice

main = Blueprint('main', __name__)


@main.route('/')
def list_invoices():
    return render_template('list.html', invoices=Invoice.objects)


@main.route('/invoice/<string:id>/detail')
def detail_invoice(id: str):
    invoice = Invoice.objects(id=id).first()
    return render_template('detail.html', invoice=invoice)


@main.route('/invoice/create', methods=['POST'])
def create_invoice():
    pdf_file = request.files['pdf']
    text = extract_text_from_pdf(pdf_file)
    summary = process_text_with_gemini(text)
    debts = json.loads(prep_text(summary.text))
    invoice = save_invoice_to_db(
        bank_name=request.form['bank_name'],
        ref_date=request.form['ref_date'],
        debts=debts,
        file_raw_text=text,
    )
    return redirect(url_for('main.detail_invoice', id=invoice.id))
