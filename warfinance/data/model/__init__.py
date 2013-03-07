"""This package holds the base SQLA-Classes whose are needed to run warfinance.

It could be use as a source to create custom working SQLA-Classes. Every
attribute/method of each SQLA-Class is mandatory.

"""
from warbase.model import Base

__all__ = ['Cost', 'Month', 'Prestation', 'Salesman']
