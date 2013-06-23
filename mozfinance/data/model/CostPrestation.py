# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from voluptuous import Schema, Required, All, Length

import Prestation, Cost


class CostPrestation(Cost.Cost):
    __tablename__ = 'costs_prestation'
    __mapper_args__ = {'polymorphic_identity': 'prestation'}
    id = Column(None, ForeignKey('costs.id'), primary_key=True)

    prestation_id = Column(Integer, ForeignKey('prestations.id'))
    prestation = relationship('Prestation')

    update_dict = set(['reason', 'amount'])  # For update purpose
    create_dict = set(['reason', 'amount', 'prestation'])


CostPrestationSchema = Schema({
    Required('reason'): All(unicode, Length(min=3, max=30)),
    Required('prestation'): Prestation.Prestation,
    'amount': float
})
