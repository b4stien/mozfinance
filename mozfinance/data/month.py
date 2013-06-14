# -*- coding: utf-8 -*-
from importlib import import_module
import datetime

from sqlalchemy.orm.exc import NoResultFound

from mozbase.util.database import db_method

import mozfinance
from . import DataRepository


class MonthData(DataRepository):
    """DataRepository object for months."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self._Month = import_module('.Month', package=self._package)

    def get(self, month_id=None, month=None, date=None,
            compute=False, create=False, **kwargs):
        """Return a month with additional attributes.

        Arguments:
            month_id -- id of the required month (*)
            month -- a month instance (*)
            date -- any datetime.date inside the required month (*)
            compute -- (bool) wether to compute missing attributes or not
            create -- (bool) wether to create a non-existent month or not

        * at least one is required

        """
        kw_month = dict()
        if month:
            kw_month['month'] = month

        elif month_id:
            kw_month['month_id'] = month_id

        # "cleanify" date provided.
        elif date:
            if not isinstance(date, datetime.date):
                raise AttributeError('date provided is not a datetime.date')

            kw_date = datetime.date(
                year=date.year,
                month=date.month,
                day=1)
            kw_month['date'] = kw_date

        try:
            month = self._get.month(**kw_month)
        except NoResultFound:
            if not create:
                raise NoResultFound
            elif not date:
                raise TypeError('create asked but no date provided')
            month = self.create(date=kw_date)

        month = self._add_attributes('month', month, compute)

        # Prestation = import_module('.Prestation', package=self._package)
        # prestas_query = self._dbsession.query(Prestation.Prestation)\
        #     .filter(Prestation.Prestation.date >= month.date)\
        #     .filter(Prestation.Prestation.date < month.next_month())

        # # Restrictions on the prestations that we will consider
        # for query_filter in mozfinance.PRESTATIONS_FILTERS:
        #     prestas_query = prestas_query.filter(query_filter)

        # prestas = prestas_query.order_by(Prestation.Prestation.date).all()
        # setattr(month, 'prestations', prestas)

        return month

    @db_method()
    def create(self, **kwargs):
        """Create and insert a month in DB. Return this month.

        Keyword arguments:
            see warfinance.data.model.Month.MonthSchema

        """
        self._Month.MonthSchema(kwargs)  # Validate datas

        month = self._Month.Month(**kwargs)
        self._dbsession.add(month)

        return month

    @db_method()
    def update(self, month_id=None, month=None, date=None,
               pop_action=False, **kwargs):
        """Update a month. Return False if there is no update or the
        updated month.

        Arguments:
            pop_action -- wether to pop an action or not
            month_id -- id of the month to update (*)
            month -- month to update (*)
            date -- date of the month to update (*)

        * at least one is required

        Keyword arguments:
            see warfinance.datamodel.Month.MonthSchema

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

        if pop_action:
            datetime_date = datetime.datetime.combine(
                _month.date, datetime.time())
            date_name = datetime_date.strftime('%B %Y').decode('utf8')
            self.action_data.create(
                message=self._Month.ACT_MONTH_UPDATE.format(date_name))

        return _month

    def remove(self, **kwargs):
        """There is no point in removing a month from DB."""
        raise NotImplementedError
