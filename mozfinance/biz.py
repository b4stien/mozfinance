# -*- coding: utf-8 -*-
"""This module provides a useful wrapper for all data objects in
mozfinance.

"""
from mozbase.data import RawDataRepository

from mozfinance.data import month, prestation, salesman, year


class BusinessWorker(RawDataRepository):
    """Business object for mozfinance. Provides all API."""

    _patch_exports = ['month', 'year', 'prestation', 'salesman']

    def __init__(self, dbsession=None, package=None):
        RawDataRepository.__init__(self, dbsession)

        self.month = month.MonthData(dbsession, package)
        self.year = year.YearData(dbsession, package)
        self.prestation = prestation.PrestationData(dbsession, package)
        self.salesman = salesman.SalesmanData(dbsession, package)
