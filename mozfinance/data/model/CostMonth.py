# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from voluptuous import Schema, Required, All, Length

import Month, Cost


class CostMonth(Cost.Cost):
    __tablename__ = 'costs_month'
    __mapper_args__ = {'polymorphic_identity': 'month'}
    id = Column(None, ForeignKey('costs.id'), primary_key=True)

    no_commission_base = Column(Boolean, default=False)

    month_id = Column(Integer, ForeignKey('months.id'))
    month = relationship('Month')

    update_dict = set(['reason', 'amount'])  # For update purpose
    create_dict = set(['reason', 'amount', 'month'])


CostMonthSchema = Schema({
    Required('reason'): All(unicode, Length(min=3, max=30)),
    Required('month'): Month.Month,
    'no_commission_base': bool,
    'amount': float
})
