# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Float, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from . import Base
import Prestation


class BillPrestation(Base):
    __tablename__ = 'bills_prestation'
    id = Column(Integer, primary_key=True)

    amount = Column(Float)
    ref = Column(Unicode(length=30))

    prestation_id = Column(Integer, ForeignKey('prestations.id'))
    prestation = relationship('Prestation', backref='bills')

    update_dict = set(['reason', 'amount'])  # For update purpose
    create_dict = set(['reason', 'amount', 'prestation'])
