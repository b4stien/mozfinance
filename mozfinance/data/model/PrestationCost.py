# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, Float, Unicode
from sqlalchemy.orm import relationship
from voluptuous import Schema, Required, All, Length

from . import Base, Prestation


class PrestationCost(Base):
    __tablename__ = 'prestation_costs'
    id = Column(Integer, primary_key=True)

    amount = Column(Float)
    reason = Column(Unicode(length=30))

    prestation_id = Column(Integer, ForeignKey('prestations.id'))
    prestation = relationship('Prestation')

    update_dict = set(['reason', 'amount'])  # For update purpose
    create_dict = set(['reason', 'amount', 'prestation'])


PrestationCostSchema = Schema({
    Required('reason'): All(unicode, Length(min=3, max=30)),
    Required('prestation'): Prestation.Prestation,
    'amount': float
})

ACT_PRESTATION_COST_CREATE = u'Ajout d\'un coût à la prestation #P{}'
ACT_PRESTATION_COST_UPDATE = u'Modification d\'un coût sur la prestation #P{}'
ACT_PRESTATION_COST_REMOVE = u'Suppression d\'un coût sur la prestation #P{}'
