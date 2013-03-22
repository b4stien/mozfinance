# -*- coding: utf-8 -*-
from datetime import date, timedelta

from sqlalchemy import Column, Integer, Date, Float
from voluptuous import Schema, Required, All, Invalid

from . import Base


class Month(Base):
    __tablename__ = "months"
    id = Column(Integer, primary_key=True)

    date = Column(Date, index=True)  # First day of the month
    cost = Column(Float)

    def next_month(self):
        """Return the date of the first day of the following month"""
        one_month = timedelta(days=31)
        in_next_month = self.date + one_month
        return date(year=in_next_month.year,
                    month=in_next_month.month,
                    day=1)

    def prev_month(self):
        """Return the date of the first day of the precedent month"""
        one_day = timedelta(days=1)
        in_prev_month = self.date - one_day
        return date(year=in_prev_month.year,
                    month=in_prev_month.month,
                    day=1)

    update_dict = set(['cost'])  # For update purpose
    create_dict = set(['date', 'cost'])


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
    'breakeven': float,
    'cost': float
})

ACT_MONTH_UPDATE = u'Modification des données du mois de {}'
