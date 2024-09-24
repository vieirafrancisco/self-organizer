from flask import Blueprint

from .models import Invoice

data = Blueprint('data', __name__)


@data.route('/data/total_debt')
def total_debt():
    total_debt = 0
    for invoice in Invoice.objects:
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        total_debt += sum([debt.value for debt in filtered_debts])

    return {'detail': total_debt}


@data.route('/data/count_debt')
def count_debt():
    count_debt = 0
    for invoice in Invoice.objects:
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        count_debt += len(filtered_debts)

    return {'detail': count_debt}


@data.route('/data/greater_debt')
def greater_debt():
    greater_debt = 0
    for invoice in Invoice.objects:
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        greater_debt = max(
            greater_debt, max([debt.value for debt in filtered_debts])
        )

    return {'detail': greater_debt}


@data.route('/data/installment_debt')
def installment_debt():
    installment_debt = 0
    for invoice in Invoice.objects:
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        installment_debt += len([
            debt.value
            for debt in filtered_debts
            if debt.total_installments > 1
        ])

    return {'detail': installment_debt}
