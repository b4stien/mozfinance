# -*- coding: utf-8 -*-
from importlib import import_module
import datetime

from mozbase.util.database import db_method

from . import DataRepository


class MonthData(DataRepository):
    """DataRepository object for months."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self._Month = import_module('.Month', package=self._package)

    def get(self, month_id=None, month=None, date=None, **kwargs):
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

            _date = datetime.date(
                year=date.year,
                month=date.month,
                day=1)

        month = self._get.month(month_id, month, _date)

        return month

    @db_method
    def create(self, **kwargs):
        """Create and insert a month in DB. Return this month.

        Keyword arguments:
            see mozfinance.data.model.Month.MonthSchema

        """
        self._Month.MonthSchema(kwargs)  # Validate datas

        month = self._Month.Month(**kwargs)
        self._dbsession.add(month)

        return month

    @db_method
    def update(self, month_id=None, month=None, date=None, **kwargs):
        """Update a month. Return False if there is no update or the
        updated month.

        Arguments:
            month_id -- id of the month to update (*)
            month -- month to update (*)
            date -- date of the month to update (*)

        * at least one is required

        Keyword arguments:
            see mozfinance.datamodel.Month.MonthSchema

        """
        _month = self._get.month(month_id, month, date)

        month_dict = {k: getattr(_month, k) for k in _month.create_dict
                      if getattr(_month, k) is not None}
        new_month_dict = month_dict.copy()

        item_to_update = [item for item in _month.update_dict if item in kwargs]

        for item in item_to_update:
            new_month_dict[item] = kwargs[item]

        self._Month.MonthSchema(new_month_dict)

        for item in item_to_update:
            setattr(_month, item, kwargs[item])

        if new_month_dict == month_dict:
            return False

        self._expire.month(month=_month)

        return _month

    def remove(self, *args, **kwargs):
        """There is no point in removing a month from DB."""
        raise NotImplementedError
