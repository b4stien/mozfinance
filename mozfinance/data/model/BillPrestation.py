# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Float, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from voluptuous import Schema, Required, All, Length

from . import Base
import Prestation


class BillPrestation(Base):
    __tablename__ = 'bills_prestation'
    id = Column(Integer, primary_key=True)

    amount = Column(Float)
    ref = Column(Unicode(length=30))

    prestation_id = Column(Integer, ForeignKey('prestations.id'))
    prestation = relationship('Prestation', backref='bills')


BillPrestationBaseDict = {
    Required('ref'): All(unicode, Length(min=3, max=30)),
    Required('amount'): float
}


BillPrestationCreateDict = BillPrestationBaseDict.copy()
BillPrestationCreateDict[Required('prestation')] = Prestation.Prestation
BillPrestationCreateSchema = Schema(BillPrestationCreateDict)


BillPrestationUpdateSchema = Schema(BillPrestationBaseDict)
