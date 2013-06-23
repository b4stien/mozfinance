# -*- coding: utf-8 -*-
"""This module provides a useful wrapper for all data objects in
mozfinance.

"""
from data import month, prestation, salesman, year


class BusinessWorker():
    """Business object for mozfinance. Provides all API."""

    def __init__(self, **kwargs):
        self.month = month.MonthData(**kwargs)
        self.year = year.YearData(**kwargs)
        self.prestation = prestation.PrestationData(**kwargs)
        self.salesman = salesman.SalesmanData(**kwargs)
