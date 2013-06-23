# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Float, Unicode, String

from . import Base


class Cost(Base):
    __tablename__ = 'costs'
    id = Column(Integer, primary_key=True)

    type = Column(String)
    __mapper_args__ = {'polymorphic_on': type}

    amount = Column(Float)
    reason = Column(Unicode(length=30))
