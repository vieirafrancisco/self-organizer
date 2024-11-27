import json
from flask import Blueprint, render_template, request, redirect, url_for

from .services import (
    extract_text_from_pdf,
    process_text_with_gemini,
    prep_text,
    save_invoice_with_debts,
)
from .models import db, Invoice

main = Blueprint('main', __name__)


@main.route('/')
def dashboard():
    invoices = db.session.execute(db.select(Invoice)).scalars().all()
    return render_template('dashboard.html', invoices=invoices)


@main.route('/invoice/list')
def list_invoice():
    invoices = db.session.execute(db.select(Invoice)).scalars().all()
    return render_template('list.html', invoices=invoices)


@main.route('/invoice/<string:id>/detail')
def detail_invoice(id: str):
    invoice = db.get_or_404(Invoice, id)
    installment_debts = [
        debt for debt in invoice.debts if debt.total_installments > 1
    ]
    sum_installment_debts = sum([debt.value for debt in installment_debts])
    debit_balance_installment_debts = sum([
        debt.value * (debt.total_installments - debt.paid_installment)
        for debt in installment_debts
    ])
    return render_template(
        'detail.html',
        invoice=invoice,
        installment_debts=installment_debts,
        sum_installment_debts=sum_installment_debts,
        debit_balance_installment_debts=debit_balance_installment_debts,
    )


@main.route('/invoice/create', methods=['POST'])
def create_invoice():
    pdf_file = request.files['pdf']
    text = extract_text_from_pdf(pdf_file)
    summary = process_text_with_gemini(text)
    debts = json.loads(prep_text(summary.text))
    invoice = save_invoice_with_debts(
        bank_name=request.form['bank_name'],
        ref_date=request.form['ref_date'],
        debts=debts,
        file_raw_text=text,
    )
    return redirect(url_for('main.detail_invoice', id=invoice.id))
