# -*- coding: utf-8 -*-
from datetime import date

from sqlalchemy import Column, Integer, Date, Unicode, Float
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from voluptuous import Schema, Required, All, Length

from . import Base


PRESTATION_CATEGORY_NONE = 0
PRESTATION_CATEGORY_SALE = 1  # eg: sale / rental
PRESTATION_CATEGORY_PRESTA = 2
PRESTATION_CATEGORY_EVENT = 3
PRESTATION_CATEGORIES = {
    PRESTATION_CATEGORY_NONE: u'Aucune',
    PRESTATION_CATEGORY_SALE: u'Vente',
    PRESTATION_CATEGORY_PRESTA: u'Prestation',
    PRESTATION_CATEGORY_EVENT: u'Evénementiel'
}
PRESTATION_SECTOR_NONE = 0
PRESTATION_SECTOR_HOSTEL = 1  # eg: bank / industry
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

    costs = relationship('PrestationCost')

    create_dict = set(['date', 'client', 'category', 'sector'])  # For update purpose
    update_dict = set(['date', 'client', 'category', 'sector'])

    def month_date(self):
        month_date = date(
            year=self.date.year,
            month=self.date.month,
            day=1)
        return month_date

    @property
    def cost(self):
        total_cost = float(0)
        for cost in self.costs:
            total_cost += cost.amount
        return total_cost

    @property
    def margin(self):
        return self.selling_price - self.cost


PrestationSchema = Schema({
    Required('date'): All(date),
    Required('client'): All(unicode, Length(min=3, max=30)),
    'category': All(int),
    'sector': All(int)
})

ACT_PRESTATION_CREATE = u'Création de #P{}'
ACT_PRESTATION_UPDATE = u'Modification de #P{}'
ACT_PRESTATION_REMOVE = u'Suppression de #P{}'
ACT_PRESTATION_SET_SELLING_PRICE = u'Modification du prix de vente de #P{}'
ACT_PRESTATION_SET_CUSTOM_COM_FORMULAE = u'Modification d\'une formule de commision sur #P{}'
ACT_PRESTATION_SET_CUSTOM_RATIOS = u'Modification d\'un coefficient de commision sur #P{}'
ACT_PRESTATION_ADD_SALESMAN = u'Ajout d\'un commercial à #P{}'
ACT_PRESTATION_REMOVE_SALESMAN = u'Suppression d\'un commercial sur #P{}'

