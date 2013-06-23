# -*- coding: utf-8 -*-
import datetime

from . import DataRepository


class YearData(DataRepository):

    def get(self, compute=False, **kwargs):
        """Return a year (ad-hoc class) with additional attributes.

        Keyword arguments:
        date -- any datetime.date of the month (required)

        """
        if 'date' in kwargs:
            if not isinstance(kwargs['date'], datetime.date):
                raise AttributeError('date provided is not a datetime.date')

        year = self._get.year(year_id=kwargs['date'].year)

        return year
