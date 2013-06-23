# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from voluptuous import Schema, Required, All, Length

import Month, Cost


class CostMonth(Cost.Cost):
    __tablename__ = 'costs_month'
    __mapper_args__ = {'polymorphic_identity': 'month'}
    id = Column(None, ForeignKey('costs.id'), primary_key=True)

    month_id = Column(Integer, ForeignKey('months.id'))
    month = relationship('Month')

    update_dict = set(['reason', 'amount'])  # For update purpose
    create_dict = set(['reason', 'amount', 'prestation'])


CostMonthSchema = Schema({
    Required('reason'): All(unicode, Length(min=3, max=30)),
    Required('prestation'): Month.Month,
    'amount': float
})
