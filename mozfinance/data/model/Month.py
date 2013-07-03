# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, Integer, Date, and_, extract
from sqlalchemy.orm import relationship, foreign, remote, backref
from voluptuous import Schema, All, Invalid

from mozbase.util.cache import cached_property

from . import Base
import Prestation
from mozfinance.util.commissions import _COMMISSIONS_VARIABLES


class Month(Base):
    __tablename__ = "months"
    id = Column(Integer, primary_key=True)

    date = Column(Date, index=True)  # First day of the month

    costs = relationship('CostMonth', lazy='dynamic')

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
        lazy='dynamic',
        backref=backref('month', uselist=False))

    _key_store_key_template = 'month:{instance.id}'
    _com_ksk_template = 'month:{instance.id}:commission_ks'

    @cached_property('month:{instance.id}:revenue')
    def revenue(self):
        """Compute and return the month's revenue."""
        revenue = float(0)
        for presta in self.prestations.all():
            if presta.selling_price is not None:
                revenue += presta.selling_price

        return revenue

    @cached_property('month:{instance.id}:total_mcost')
    def total_month_cost(self):
        """Compute and return the sum of all the costs (CostMonth)
        associated with this month.

        """
        total_mcost = float(0)
        for cost in self.costs.all():
            total_mcost += cost.amount

        return total_mcost

    @cached_property('month:{instance.id}:total_pcost')
    def total_prestation_cost(self):
        """Compute and return the sum of the costs of all the prestation
        in this month.

        """
        total_pcost = float(0)
        for presta in self.prestations.all():
            total_pcost += presta.total_cost

        return total_pcost

    @cached_property('month:{instance.id}:gross_margin')
    def gross_margin(self):
        """Compute and return the month's gross margin."""
        return self.revenue - self.total_prestation_cost

    @cached_property('month:{instance.id}:net_margin')
    def net_margin(self):
        """Compute and return the month's net margin."""
        return self.gross_margin - self.total_month_cost

    @cached_property('month:{instance.id}:commission_base')
    def commission_base(self):
        """Compute and return the month's commission base."""
        import CostMonth

        commission_base = self.gross_margin
        costs_in_bc = self.costs\
            .filter(CostMonth.CostMonth.no_commission_base == False)

        for cost in costs_in_bc.all():
            commission_base -= cost.amount

        return commission_base

    @property
    def commissions_variables(self):
        """Return a dict of the available variables for monthly
        commissions computations.

        """
        vars = dict()

        for key in _COMMISSIONS_VARIABLES['month']:
            a_var = _COMMISSIONS_VARIABLES['month'][key]
            vars[key] = getattr(self, a_var['attr'])

        return vars

    @property
    def month_salesmen(self):
        """Return a list of all the month-salesman association of this
        month.

        """
        from FakeAssMonthSalesman import MonthSalesman

        salesmen = []
        for prestation in self.prestations:
            for presta_sm in prestation.prestation_salesmen:
                if not presta_sm.salesman in salesmen:
                    salesmen.append(presta_sm.salesman)

        month_salesmen = []
        for salesman in salesmen:
            month_salesmen.append(MonthSalesman(self, salesman))

        return month_salesmen


def MonthDate(msg=None):
    """Verify that the value is a correct month date."""
    def f(v):
        if v.day != 1:
            raise Invalid(msg or 'expected a date with date.day == 1')
        else:
            return v
    return f

MonthDateSchema = Schema(All(datetime.date, MonthDate()))
