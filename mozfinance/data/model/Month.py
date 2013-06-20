# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, Integer, Date, Float, and_, extract
from sqlalchemy.orm import relationship, foreign, remote
from voluptuous import Schema, Required, All, Invalid

from . import Base
import Prestation


class Month(Base):
    __tablename__ = "months"
    id = Column(Integer, primary_key=True)

    date = Column(Date, index=True)  # First day of the month

    cost = Column(Float)
    taxes = Column(Float)
    salaries = Column(Float)
    commissions_refined = Column(Float)

    _primaryjoin = and_(
        remote(
            extract('year', Prestation.Prestation.date)
        ) == foreign(
            extract('year', date)
        ), remote(
            extract('month', Prestation.Prestation.date)
        ) == foreign(
            extract('month', date)))
    prestations = relationship(
        'Prestation',
        primaryjoin=_primaryjoin,
        viewonly=True,
        uselist=True,
        lazy='dynamic')

    @property
    def next_month(self):
        """Return the date of the first day of the following month"""
        one_month = datetime.timedelta(days=31)
        in_next_month = self.date + one_month
        return datetime.date(year=in_next_month.year,
                    month=in_next_month.month,
                    day=1)

    @property
    def prev_month(self):
        """Return the date of the first day of the precedent month"""
        one_day = datetime.timedelta(days=1)
        in_prev_month = self.date - one_day
        return datetime.date(year=in_prev_month.year,
                    month=in_prev_month.month,
                    day=1)

    update_dict = set(['cost', 'salaries', 'taxes', 'commissions_refined'])  # For update purpose
    create_dict = set(['date', 'cost', 'salaries', 'taxes', 'commissions_refined'])


def MonthDate(msg=None):
    """Verify that the value is a correct month date."""
    def f(v):
        if v.day != 1:
            raise Invalid(msg or 'expected a date with date.day == 1')
        else:
            return v
    return f

MonthSchema = Schema({
    Required('date'): All(datetime.date, MonthDate()),
    'cost': float,
    'taxes': float,
    'salaries': float,
    'commissions_refined': float
})

ACT_MONTH_UPDATE = u'Modification des données du mois de {}'
