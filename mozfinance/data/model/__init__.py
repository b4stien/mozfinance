# -*- coding: utf-8 -*-
"""This package holds the base SQLA-Classes whose are needed to run
mozfinance.

It could be use as a source to create custom working SQLA-Classes. Every
attribute/method of each SQLA-Class is mandatory.

"""
from sqlalchemy.ext.declarative import declarative_base


__all__ = ['User', 'Prestation', 'Month', 'Salesman', 'Cost', 'CostPrestation', 'CostMonth', 'AssPrestationSalesman']


Base = declarative_base()
