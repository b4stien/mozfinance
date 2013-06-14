# -*- coding: utf-8 -*-
import datetime

from mozbase.util.cache import Cache
from mozbase.util.cache_systems.database_cache import DatabaseCache

from mozfinance.data.model.Prestation import Prestation
from mozfinance.data.model.PrestationCost import PrestationCost
from mozfinance.data.subworkers.compute import ComputeWorker
from mozfinance.biz import BusinessWorker

from . import TestData


class TestBusinessCompute(TestData):

    def setUp(self):
        TestData.setUp(self)
        cache = Cache()
        cache.append_cache(DatabaseCache(dbsession=self.dbsession))
        self.biz = BusinessWorker(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user,
            cache=cache)

        self._compute = ComputeWorker(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user,
            cache=cache)

    def tearDown(self):
        TestData.tearDown(self)
        del self.biz

    def test_get_month_revenue_with_none_presta_selling_price(self):
        now = datetime.datetime.now()
        now_date = now.date()
        self.month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.biz.month.create(date=self.month_date)
        presta1 = Prestation(date=now_date)
        presta2 = Prestation(date=now_date, selling_price=float(16))
        self.dbsession.add(presta1)
        self.dbsession.add(presta2)
        self.dbsession.flush()
        month = self.biz.month.get(date=self.month_date, compute=True)
        self.assertEqual(month.revenue, float(16))


class TestBusinessWithDatas(TestData):

    def setUp(self):
        TestData.setUp(self)
        cache = Cache()
        cache.append_cache(DatabaseCache(dbsession=self.dbsession))
        self.biz = BusinessWorker(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user,
            cache=cache)
        self.dbsession.delete(self.prestation)
        self.dbsession.flush()

        self._compute = ComputeWorker(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user,
            cache=cache)

    def tearDown(self):
        TestData.tearDown(self)
        del self.biz

    def test_get_computed_values(self):
        now = datetime.datetime.now()
        now_date = now.date()
        self.month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.biz.month.create(date=self.month_date, cost=float(3))
        presta1 = Prestation(date=now_date, selling_price=float(12))
        presta2 = Prestation(date=now_date, selling_price=float(16))
        self.dbsession.add(presta1)
        self.dbsession.add(presta2)
        self.dbsession.flush()
        cost1 = PrestationCost(prestation=presta1, amount=float(4))
        self.dbsession.add(cost1)
        self.dbsession.flush()
        month = self.biz.month.get(date=self.month_date, compute=True)
        presta = self.biz.prestation.get(prestation=presta1, compute=True)
        self.assertEqual(month.revenue, float(28))
        self.assertEqual(month.total_cost, float(4))
        self.assertEqual(month.gross_margin, float(24))
        self.assertEqual(month.net_margin, float(21))
        self.assertEqual(len(month.prestations.all()), 2)
        self.assertEqual(presta.cost, float(4))

    def test_compute_year_net_margin(self):
        month_date = datetime.date(year=2013, month=1, day=1)
        another_month_date = datetime.date(year=2013, month=2, day=1)

        self.biz.month.create(
            date=month_date,
            cost=float(1000))
        self.biz.month.create(
            date=another_month_date,
            cost=float(2000))

        presta = Prestation(
            date=month_date,
            selling_price=float(3000),
            category=0,
            sector=0)
        self.dbsession.add(presta)
        another_presta = Prestation(
            date=another_month_date,
            selling_price=float(4000),
            category=0,
            sector=0)
        self.dbsession.add(another_presta)
        self.dbsession.commit()

        year_net_margin = self._compute.year_net_margin(date=month_date)

        self.assertEqual(year_net_margin, float(4000))

        year = self.biz.year.get(date=another_month_date)

        self.assertEqual(year.net_margin, float(4000))
