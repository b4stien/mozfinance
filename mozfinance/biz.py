# -*- coding: utf-8 -*-
"""This module provides a useful wrapper for all data objects in
mozfinance.

"""
from mozbase.data import RawDataRepository

from mozfinance.data import month, prestation, salesman, year


class BusinessObject(RawDataRepository):
    """Business object for mozfinance. Provides all API."""

    _patch_exports = ['month', 'year', 'prestation', 'salesman']

    def __init__(self, dbsession=None, package=None):
        RawDataRepository.__init__(self, dbsession)
        self._package = package

        self.month = month.MonthData(self)
        self.year = year.YearData(self)
        self.prestation = prestation.PrestationData(self)
        self.salesman = salesman.SalesmanData(self)
