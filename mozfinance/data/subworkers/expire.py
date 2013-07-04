# -*- coding: utf-8 -*-
"""Module in charge of expiring values in cache to respond to certain
interactions with database.

A part of the dependency map is "written" here in methods. The rest of
this map is directly into model's object, with the key_store mechanism.

"""

from dogpile.cache.api import NoValue

from mozbase.data import RawDataRepository
from mozfinance.data.subworkers.get import GetWorker


class ExpireWorker(RawDataRepository):

    def __init__(self, dbsession=None, package=None, **kwargs):
        RawDataRepository.__init__(self, dbsession)
        self._package = package
        self._get = GetWorker(dbsession=dbsession, package=package)

    def _expire_instance(self, instance, ksk_tpl_name=None):
        """Expire every key related to an instance by deleting every key
        stored in its key_store.

        Argument:
            ksk_tpl_name -- default: _key_store_key_template
                            name of the attribute in which is saved the
                            template of the key store's key.

        """
        format_dict = dict()
        format_dict['instance'] = instance

        if ksk_tpl_name is None:
            ksk_tpl_name = '_key_store_key_template'

        key_store_key = getattr(instance, ksk_tpl_name).format(**format_dict)

        key_store = self._dbsession.cache.get(key_store_key)
        if isinstance(key_store, NoValue):
            key_store = []

        for key in key_store:
            self._dbsession.cache.delete(key)

    def prestation(self, prestation_id=None, prestation=None, **kwargs):
        """Expire the given prestation and its month."""
        presta = self._get.prestation(prestation_id, prestation)
        self._expire_instance(presta)
        self.month(month=presta.month)

    def month(self, month_id=None, month=None, date=None, **kwargs):
        """Expire the given month, its year and every
        prestation-salesman association of this month.

        """
        month = self._get.month(month_id, month, date)
        self._expire_instance(month)

        prestas = month.prestations.all()
        for presta in prestas:
            for presta_sm in presta.prestation_salesmen:
                self._expire_instance(presta_sm)

            self._expire_instance(presta, '_com_ksk_template')

        self._expire_instance(month, '_com_ksk_template')
        self.month_salesmen(month=month)

        self.year(year_id=month.date.year)

    def year(self, year_id=None, year=None, date=None, **kwargs):
        """Expire the given year."""
        year = self._get.year(year_id, year, date)
        self._expire_instance(year)

    def prestation_salesmen(self, prestation_id=None, prestation=None, **kwargs):
        """Expire every prestation-salesman association of the given
        prestation, and every month-salesman association of the given
        prestation's month.

        Also expire the commission's key store of the prestation and the
        one of the prestation's month.

        """
        presta = self._get.prestation(prestation_id, prestation)

        for presta_sm in presta.prestation_salesmen:
            self._expire_instance(presta_sm)

        self._expire_instance(presta, '_com_ksk_template')
        self._expire_instance(presta.month, '_com_ksk_template')

        self.month_salesmen(month=presta.month)


    def month_salesmen(self, month_id=None, month=None, date=None, **kwargs):
        """Expire every month-salesman association of the given month."""
        month = self._get.month(month_id, month, date)

        for month_sm in month.month_salesmen:
            self._expire_instance(month_sm)
