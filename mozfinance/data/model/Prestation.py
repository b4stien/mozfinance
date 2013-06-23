# -*- coding: utf-8 -*-
from datetime import date

from sqlalchemy import Column, Integer, Date, Unicode, Float
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, object_session
from voluptuous import Schema, Required, All, Length

from mozbase.util.cache import cached_property

from . import Base
import Month
from mozfinance.util.commissions import _COMMISSIONS_VARIABLES


PRESTATION_CATEGORY_NONE = 0
PRESTATION_CATEGORY_SALE = 1
PRESTATION_CATEGORY_PRESTA = 2
PRESTATION_CATEGORY_EVENT = 3
PRESTATION_CATEGORIES = {
    PRESTATION_CATEGORY_NONE: u'Aucune',
    PRESTATION_CATEGORY_SALE: u'Vente',
    PRESTATION_CATEGORY_PRESTA: u'Prestation',
    PRESTATION_CATEGORY_EVENT: u'Evénementiel'
}
PRESTATION_SECTOR_NONE = 0
PRESTATION_SECTOR_HOSTEL = 1
PRESTATION_SECTOR_AGENCY = 2
PRESTATION_SECTOR_ADVERTISEUR = 3
PRESTATION_SECTORS = {
    PRESTATION_SECTOR_NONE: u'Aucun',
    PRESTATION_SECTOR_HOSTEL: u'Hôtellerie/Restauration',
    PRESTATION_SECTOR_AGENCY: u'Agences',
    PRESTATION_SECTOR_ADVERTISEUR: u'Annonceurs'
}


class Prestation(Base):
    __tablename__ = "prestations"
    id = Column(Integer, primary_key=True)

    date = Column(Date, index=True)
    client = Column(Unicode(length=30))
    selling_price = Column(Float)

    salesmen = association_proxy('prestation_salesmen', 'salesman')

    category = Column(Integer, index=True, default=PRESTATION_CATEGORY_NONE)
    sector = Column(Integer, index=True, default=PRESTATION_SECTOR_NONE)

    costs = relationship('CostPrestation')

    create_dict = set(['date', 'client', 'category', 'sector'])  # For update purpose
    update_dict = set(['date', 'client', 'category', 'sector'])

    _key_store_key_template = 'prestation:{instance.id}'
    _com_ksk_template = 'prestation:{instance.id}:commission_ks'

    @property
    def month_date(self):
        """Return the date of the prestation's month."""
        month_date = date(
            year=self.date.year,
            month=self.date.month,
            day=1)
        return month_date

    @property
    def month(self):
        """Return the prestation's month."""
        month = object_session(self).query(Month.Month)\
            .filter(Month.Month.date == self.month_date)\
            .one()
        return month

    @cached_property('prestation:{instance.id}:total_cost')
    def total_cost(self):
        """Compute and return the sum of the costs of this prestation."""
        total_cost = float(0)
        for cost in self.costs:
            total_cost += cost.amount
        return total_cost

    @cached_property('prestation:{instance.id}:margin')
    def margin(self):
        """Compute and return the prestation's margin."""
        return self.selling_price - self.total_cost

    @cached_property(
        'prestation:{instance.id}:total_commission',
        ksk_tpl=[_key_store_key_template, 'month:{instance.month.id}'])
    def total_commission(self):
        """Compute and return the prestation's margin."""
        tc = float(0)
        for prestat_sm in self.prestation_salesmen:
            tc += tc.commission

        return tc

    @property
    def commissions_variables(self):
        """Return a dict of the available variables for prestation-level
        commissions computations.

        """
        vars = self.month.commissions_variables

        for key in _COMMISSIONS_VARIABLES['prestation']:
            a_var = _COMMISSIONS_VARIABLES['prestation'][key]
            vars[key] = getattr(self, a_var['attr'])

        return vars

PrestationSchema = Schema({
    Required('date'): All(date),
    Required('client'): All(unicode, Length(min=3, max=30)),
    'category': All(int),
    'sector': All(int)
})
