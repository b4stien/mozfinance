# -*- coding: utf-8 -*-
from sqlalchemy import extract
from sqlalchemy.orm import object_session

from mozbase.util.cache import cached_property

import mozfinance
from AssPrestationSalesman import PrestationSalesman
import Prestation


class MonthSalesman(object):

    def __init__(self, month, salesman):
        self.month = month
        self.salesman = salesman
        self._cache = object_session(self.month).cache

    _key_store_key_template = 'month:{instance.month.id}:salesman:{instance.salesman.id}'

    @cached_property(
        'month:{instance.month.id}:salesman:{instance.salesman.id}:commission_prestations',
        cache='_cache')
    def commission_prestations(self):
        """Compute and return the sum of the prestations' commissions
        for this salesman during this month.

        """
        presta_sms = self.salesman.salesman_prestations\
            .join(PrestationSalesman.prestation)\
            .filter(extract('year', Prestation.Prestation.date) == self.month.date.year)\
            .filter(extract('month', Prestation.Prestation.date) == self.month.date.month)\
            .all()

        commission_prestations = float(0)
        for presta_sm in presta_sms:
            commission_prestations += presta_sm.commission

        return commission_prestations

    @cached_property(
        'month:{instance.month.id}:salesman:{instance.salesman.id}:commission_bonuses',
        cache='_cache')
    def commission_bonuses(self):
        """Compute and return the sum of the bonuses' commissions
        for this salesman during this month.

        """
        commission_bonuses = float(0)

        for bonus in mozfinance.COMMISSIONS_BONUSES:
            commission_bonuses += bonus(**self.month.commissions_variables)

        return commission_bonuses

    @cached_property(
        'month:{instance.month.id}:salesman:{instance.salesman.id}:commission_total',
        cache='_cache')
    def commission_total(self):
        """Compute and return the summ of all kind of commissions for
        this salesman regarding this month.

        """
        return self.commission_prestations + self.commission_bonuses