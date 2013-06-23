# -*- coding: utf-8 -*-
import datetime

from sqlalchemy.sql import extract

from mozbase.util.cache import cached_property

import Month


class Year(object):

    _key_store_key_template = 'year:{instance.id}'

    def __init__(self, id, dbsession):
        self.id = id
        self.date = datetime.date(year=id, month=1, day=1)
        self._dbsession = dbsession
        self._cache = dbsession.cache

    @property
    def months(self):
        """Return all the months of this year. May go into future."""
        months = self._dbsession.query(Month.Month)\
            .filter(extract('year', Month.Month.date) == self.id)\
            .all()
        return months

    @cached_property('year:{instance.id}:revenue', cache='_cache')
    def revenue(self):
        """Compute and return the revenue of this year."""
        revenue = float(0)
        for month in self.months:
            revenue += month.revenue

        return revenue

    @cached_property('year:{instance.id}:gross_margin', cache='_cache')
    def gross_margin(self):
        """Compute and return the gross margin of this year."""
        gross_margin = float(0)
        for month in self.months:
            gross_margin += month.gross_margin

        return gross_margin

    @cached_property('year:{instance.id}:net_margin', cache='_cache')
    def net_margin(self):
        """Compute and return the net margin of this year."""
        net_margin = float(0)
        for month in self.months:
            net_margin += month.net_margin

        return net_margin
