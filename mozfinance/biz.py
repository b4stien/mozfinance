# -*- coding: utf-8 -*-
"""This module provides a useful wrapper for all data objects in
mozfinance.

"""
from mozbase.data import RawDataRepository

from mozfinance.data import month, prestation, salesman, year


class BusinessWorker(RawDataRepository):
    """Business object for mozfinance. Provides all API."""

    _patch_exports = ['month', 'year', 'prestation', 'salesman']

    def __init__(self, dbsession=None, user_id=None, user=None, package=None):
        RawDataRepository.__init__(self, dbsession)

        kwargs = dict(
            dbsession=dbsession,
            user_id=user_id,
            user=user,
            package=package)

        self.month = month.MonthData(**kwargs)
        self.year = year.YearData(**kwargs)
        self.prestation = prestation.PrestationData(**kwargs)
        self.salesman = salesman.SalesmanData(**kwargs)
