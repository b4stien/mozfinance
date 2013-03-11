 # -*- coding: utf-8 -*-
import unittest
import datetime

from warfinance.data.model.Prestation import Prestation
from warfinance.data.model.Cost import Cost
from warfinance.data.model.Month import Month
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
        self.biz.data.months.create(date=self.month_date, breakeven=float(3))
        presta1 = Prestation(date=now_date, selling_price=float(12))
        presta2 = Prestation(date=now_date, selling_price=float(16))
        self.session.add(presta1)
        self.session.add(presta2)
        self.session.flush()
        cost1 = Cost(prestation=presta1, amount=float(4))
        self.session.add(cost1)
        self.session.flush()
        month = self.biz.get.month(date=self.month_date, compute=True)
        presta = self.biz.get.prestation(prestation=presta1, compute=True)
        self.assertEqual(month.revenu, float(28))
        self.assertEqual(month.total_cost, float(4))
        self.assertEqual(month.gross_margin, float(24))
        self.assertEqual(month.commission_base, float(21))
        self.assertEqual(len(month.prestations), 2)
        self.assertEqual(presta.cost, float(4))
