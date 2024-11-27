import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Debt(db.Model):
    __tablename__ = 'debt'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    description: Mapped[str]
    value: Mapped[float]
    paid_installment: Mapped[int]
    total_installments: Mapped[int]

    invoice_id: Mapped[int] = mapped_column(ForeignKey('invoice.id'))
    invoice: Mapped['Invoice'] = relationship(back_populates='debts')


class Invoice(db.Model):
    __tablename__ = 'invoice'

    id: Mapped[int] = mapped_column(primary_key=True)
    bank_name: Mapped[str]
    ref_date: Mapped[datetime.date] = mapped_column(Date)
    file_raw_text: Mapped[str]

    debts: Mapped[list['Debt']] = relationship(back_populates='invoice')

    def __repr__(self):
        return f'{self.bank_name} - {self.ref_date}'
