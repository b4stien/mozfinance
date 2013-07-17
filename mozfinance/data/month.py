# -*- coding: utf-8 -*-
from importlib import import_module
import datetime

from sqlalchemy.orm import joinedload

from mozbase.util.database import db_method

from mozfinance.data import cost
from . import DataRepository


class MonthData(DataRepository):
    """DataRepository object for months."""

    def __init__(self, bo=None):
        DataRepository.__init__(self, bo)
        self._Month = import_module('.Month', package=self._package)

        self.cost = cost.CostMonthData(bo)
        self.salesman = MonthSalesmanRepository(bo)

    def _get(self, month_id=None, month=None, date=None):
        """Return a month given a month, a month_id or a date."""
        if month:
            if not isinstance(month, self._Month.Month):
                raise AttributeError('month provided is not a wb-Month')

            return month

        elif month_id:
            return self._dbsession.query(self._Month.Month)\
                .filter(self._Month.Month.id == month_id)\
                .one()

        elif date:
            if not isinstance(date, datetime.date):
                raise AttributeError('date provided is not a datetime.date')

            return self._dbsession.query(self._Month.Month)\
                .filter(self._Month.Month.date == date)\
                .one()

        else:
            raise TypeError(
                'Month informations (month, month_id or date) not provided')

    def get(self, month_id=None, month=None, date=None, **kwargs):
        """Return a month. Can accept extra arguments.

        Arguments:
            month_id -- id of the required month (*)
            month -- a month instance (*)
            date -- any datetime.date inside the required month (*)

        * at least one is required

        """
        if date:
            if not isinstance(date, datetime.date):
                raise AttributeError('date provided is not a datetime.date')

            date = datetime.date(
                year=date.year,
                month=date.month,
                day=1)

        return self._get(month_id, month, date)

    def _expire(self, month_id=None, month=None, date=None):
        """Expire the given month, its year and every PrestationSalesman
        association of this month.

        """
        month = self._get(month_id, month, date)
        self._expire_instance(month)

        month_prestations = month.prestations.options(joinedload('prestation_salesmen'))
        for presta in month_prestations:
            for presta_sm in presta.prestation_salesmen:
                self._expire_instance(presta_sm)

            self._expire_instance(presta, '_com_ksk_template')

        self._expire_instance(month, '_com_ksk_template')
        self.salesman._expire(month=month)

        self._bo.year._expire(year_id=month.date.year)

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


class MonthSalesmanRepository(DataRepository):

    def _expire(self, month_id=None, month=None, date=None):
        """Expire every MonthSalesman association of the given month."""
        month = self._bo.month._get(month_id, month, date)

        for month_sm in month.month_salesmen:
            self._expire_instance(month_sm)
