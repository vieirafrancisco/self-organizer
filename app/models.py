import mongoengine as me

from .settings import MONGODB_URI

me.connect(host=MONGODB_URI)


class Debt(me.EmbeddedDocument):
    date = me.StringField()
    description = me.StringField()
    value = me.DecimalField()
    paid_installment = me.IntField()
    total_installments = me.IntField()


class Invoice(me.Document):
    bank_name = me.StringField()
    ref_date = me.DateField()
    debts = me.EmbeddedDocumentListField(Debt)
    file_raw_text = me.StringField()
