# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, Float, Unicode
from sqlalchemy.orm import relationship
from voluptuous import Schema, Required, All, Length

from . import Base, Prestation


class Cost(Base):
    __tablename__ = 'costs'
    id = Column(Integer, primary_key=True)

    amount = Column(Float)
    reason = Column(Unicode(length=30))
