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
def dashboard():
    total_debt = 0
    count_debt = 0
    greater_debt = 0
    installment_debt = 0
    for invoice in Invoice.objects:
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        total_debt += sum([debt.value for debt in filtered_debts])
        count_debt += len(filtered_debts)
        greater_debt = max(
            greater_debt, max([debt.value for debt in filtered_debts])
        )
        installment_debt += len([
            debt.value
            for debt in filtered_debts
            if debt.total_installments > 1
        ])

    return render_template(
        'dashboard.html',
        total_debt=round(total_debt, 2),
        count_debt=count_debt,
        greater_debt=greater_debt,
        installment_debt=installment_debt,
    )


@main.route('/invoice/list')
def list_invoice():
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
