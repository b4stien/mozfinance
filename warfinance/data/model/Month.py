# -*- coding: utf-8 -*-
from datetime import date

from sqlalchemy import Column, Integer, Date, Float
from voluptuous import Schema, Required, All, Length, Invalid

from . import Base


class Month(Base):
    __tablename__ = "months"
    id = Column(Integer, primary_key=True)

    date = Column(Date, index=True)  # First day of the month
    breakeven = Column(Float)

    def next_month(self):
        next_month = date(year=self.date.year,
                          month=self.date.month+1,
                          day=self.date.day)
        return next_month

    update_dict = set(['breakeven'])  # For update purpose
    create_dict = set(['date', 'breakeven'])


def MonthDate(msg=None):
    """Verify that the value is a correct month date."""
    def f(v):
        if v.day != 1:
            raise Invalid(msg or 'expected a date with date.day == 1')
        else:
            return v
    return f

MonthSchema = Schema({
    Required('date'): All(date, MonthDate()),
    'breakeven': float
})

ACT_MONTH_UPDATE = u'Modification des données du mois de {}'
