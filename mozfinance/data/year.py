# -*- coding: utf-8 -*-
import datetime
from importlib import import_module

from . import DataRepository


class YearData(DataRepository):

    def _get(self, year_id=None, year=None, date=None):
        """Return a year (specific object) given a date or a year number."""
        Year = import_module('.FakeYear', package=self._package)

        if year:
            if not isinstance(year, Year.Year):
                raise AttributeError('year provided is not a correct Year')

            return year

        elif date:
            if not isinstance(date, datetime.date):
                raise AttributeError('year provided is not a datetime.date')
            if not date.month == 1 or not date.day == 1:
                raise AttributeError('date provided is not correct')
            year = Year.Year(date.year, self._dbsession)
            return year

        elif year_id:
            if not isinstance(year_id, int):
                raise AttributeError('year_id provided is not an int')
            year = Year.Year(year_id, self._dbsession)
            return year

        else:
            raise TypeError('year informations not provided')

    def get(self, date=None, **kwargs):
        """Return a year (ad-hoc class) with additional attributes.

        Keyword arguments:
        date -- any datetime.date of the month (required)

        """
        if date is None:
            raise TypeError('date not provided')

        if not isinstance(date, datetime.date):
            raise AttributeError('date provided is not a datetime.date')

        return self._get(year_id=date.year)

    def _expire(self, year_id=None, year=None, date=None):
        """Expire the given year."""
        year = self._get(year_id, year, date)
        self._expire_instance(year)
