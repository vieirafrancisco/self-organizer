from flask import Blueprint

from .models import Invoice

data = Blueprint('data', __name__)


@data.route('/data/total_debt')
def total_debt():
    total_debt = 0
    for invoice in Invoice.query.all():
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        total_debt += sum([debt.value for debt in filtered_debts])

    return {'detail': total_debt}


@data.route('/data/count_debt')
def count_debt():
    count_debt = 0
    for invoice in Invoice.query.all():
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        count_debt += len(filtered_debts)

    return {'detail': count_debt}


@data.route('/data/greater_debt')
def greater_debt():
    greater_debt = 0
    for invoice in Invoice.query.all():
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        if filtered_debts:
            greater_debt = max(
                greater_debt, max([debt.value for debt in filtered_debts])
            )

    return {'detail': greater_debt}


@data.route('/data/count_installment_debts')
def count_installment_debts():
    count = 0
    for invoice in Invoice.query.all():
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        count += len([
            debt.value
            for debt in filtered_debts
            if debt.total_installments > 1
        ])

    return {'detail': count}


@data.route('/data/sum_installment_debts')
def sum_installment_debts():
    _sum = 0
    for invoice in Invoice.query.all():
        filtered_debts = [debt for debt in invoice.debts if debt.value > 0]
        _sum += sum([
            debt.value
            for debt in filtered_debts
            if debt.total_installments > 1
        ])

    return {'detail': _sum}
