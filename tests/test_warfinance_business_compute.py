 # -*- coding: utf-8 -*-
import datetime

from warfinance.data.model.Prestation import Prestation
from warfinance.data.model.PrestationCost import PrestationCost
from warfinance.biz import BusinessWorker

from . import TestData


class TestBusinessCompute(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.biz = BusinessWorker(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        del self.biz

    def test_get_month_revenu_with_none_presta_selling_price(self):
        now = datetime.datetime.now()
        now_date = now.date()
        self.month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.biz.data.months.create(date=self.month_date)
        presta1 = Prestation(date=now_date)
        presta2 = Prestation(date=now_date, selling_price=float(16))
        self.session.add(presta1)
        self.session.add(presta2)
        self.session.flush()
        month = self.biz.get.month(date=self.month_date, compute=True)
        self.assertEqual(month.revenu, float(16))


class TestBusinessWithDatas(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.biz = BusinessWorker(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        del self.biz

    def test_get_computed_values(self):
        now = datetime.datetime.now()
        now_date = now.date()
        self.month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.biz.data.months.create(date=self.month_date, cost=float(3))
        presta1 = Prestation(date=now_date, selling_price=float(12))
        presta2 = Prestation(date=now_date, selling_price=float(16))
        self.session.add(presta1)
        self.session.add(presta2)
        self.session.flush()
        cost1 = PrestationCost(prestation=presta1, amount=float(4))
        self.session.add(cost1)
        self.session.flush()
        month = self.biz.get.month(date=self.month_date, compute=True)
        presta = self.biz.get.prestation(prestation=presta1, compute=True)
        self.assertEqual(month.revenu, float(28))
        self.assertEqual(month.total_cost, float(4))
        self.assertEqual(month.gross_margin, float(24))
        self.assertEqual(month.net_margin, float(21))
        self.assertEqual(len(month.prestations), 2)
        self.assertEqual(presta.cost, float(4))

    def test_compute_year_net_margin(self):
        month_date = datetime.date(year=2013, month=1, day=1)
        another_month_date = datetime.date(year=2013, month=2, day=1)

        self.biz.data.months.create(
            date=month_date,
            cost=float(1000))
        self.biz.data.months.create(
            date=another_month_date,
            cost=float(2000))

        presta = Prestation(
            date=month_date,
            selling_price=float(3000),
            category=0,
            sector=0)
        self.session.add(presta)
        another_presta = Prestation(
            date=another_month_date,
            selling_price=float(4000),
            category=0,
            sector=0)
        self.session.add(another_presta)

        year_net_margin = self.biz._compute.year_net_margin(date=month_date)

        self.assertEqual(year_net_margin, float(4000))

        year = self.biz.get.year(date=another_month_date)

        self.assertEqual(year.net_margin, float(4000))
