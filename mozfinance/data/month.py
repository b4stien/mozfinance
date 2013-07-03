# -*- coding: utf-8 -*-
from importlib import import_module
import datetime

from mozbase.util.database import db_method

from mozfinance.data import cost
from . import DataRepository


class MonthData(DataRepository):
    """DataRepository object for months."""

    def __init__(self, dbsession=None, package=None):
        DataRepository.__init__(self, dbsession, package)
        self._Month = import_module('.Month', package=self._package)

        self.cost = cost.CostMonthData(dbsession, package)

    def get(self, month_id=None, month=None, date=None):
        """Return a month.

        Arguments:
            month_id -- id of the required month (*)
            month -- a month instance (*)
            date -- any datetime.date inside the required month (*)

        * at least one is required

        """
        # "cleanify" date provided.
        if date:
            if not isinstance(date, datetime.date):
                raise AttributeError('date provided is not a datetime.date')

            date = datetime.date(
                year=date.year,
                month=date.month,
                day=1)

        month = self._get.month(month_id, month, date)

        return month

    @db_method
    def create(self, date=None):
        """Create and insert a month in DB. Return this month.

        Arguments:
            date -- the datetime.date of the first day of the month we
                    want to create

        """
        self._Month.MonthDateSchema(date)  # Validate datas

        month = self._Month.Month(date=date)
        self._dbsession.add(month)

        return month

    def update(self, *args, **kwargs):
        """There is not point in updating a month."""
        raise NotImplementedError

    def remove(self, *args, **kwargs):
        """There is no point in removing a month from DB."""
        raise NotImplementedError
