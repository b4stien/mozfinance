# -*- coding: utf-8 -*-
"""This package holds the base SQLA-Classes whose are needed to run
mozfinance.

It could be use as a source to create custom working SQLA-Classes. Every
attribute/method of each SQLA-Class is mandatory.

"""
from mozbase.model import Base

__all__ = ['Month', 'Prestation', 'Salesman', 'Cost', 'CostPrestation', 'CostMonth', 'AssPrestationSalesman']
