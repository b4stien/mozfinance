# -*- coding: utf-8 -*-
from importlib import import_module

from sqlalchemy.orm.exc import NoResultFound

from mozbase.data import RawDataRepository
from mozfinance.data.subworkers.get import GetWorker


class ExpireWorker(RawDataRepository):

    def __init__(self, dbsession=None, package=None, cache=None, **kwargs):
        RawDataRepository.__init__(self, dbsession)
        self._cache = cache
        self._package = package
        self._get = GetWorker(dbsession=dbsession, package=package)


    def prestation(self, prestation_id=None, prestation=None, **kwargs):
        presta = self._get.prestation(prestation_id, prestation)
        self._cache.expire(key='prestation:{}:'.format(presta.id))
        self.month(date=presta.month_date())

    def month(self, month_id=None, month=None, date=None, **kwargs):
        try:
            month = self._get.month(month_id, month, date)
        except NoResultFound:
            return

        # To expire commissions
        prestas = month.prestations.all()
        for presta in prestas:
            self.prestation_salesman(prestation=presta)

        self._cache.expire(key='month:{}:'.format(month.id))

        self.year(year_id=month.date.year)

    def all_months(self):
        Month = import_module('.Month', package=self._package)
        months = self._dbsession.query(Month.Month).all()

        for month in months:
            self.month(month=month)

    def year(self, year_id=None, year=None, date=None, **kwargs):
        year = self._get.year(year_id, year, date)
        self._cache.expire(key='year:{}:'.format(year.id))

    def prestation_salesman(self, prestation_id=None, prestation=None, **kwargs):
        presta = self._get.prestation(prestation_id, prestation)
        self._cache.expire(key='prestation:{}:salesmen_com'.format(presta.id))
        self.month_salesman(date=presta.month_date())

    def month_salesman(self, month_id=None, month=None, date=None, **kwargs):
        try:
            month = self._get.month(month_id, month, date)
        except NoResultFound:
            return
        self._cache.expire(key='month:{}:salesmen_com'.format(month.id))
