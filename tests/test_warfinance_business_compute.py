 # -*- coding: utf-8 -*-
import unittest
import datetime

from warfinance.data.model.Prestation import Prestation
from warfinance.data.model.Cost import Cost
from warfinance.data.model.Month import Month
from warfinance.data.months import MonthsData
from warfinance.biz import BusinessWorker

from . import TestData


class TestBusinessCompute(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.biz = BusinessWorker(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)
        self.months_data = MonthsData(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        del self.biz
        del self.months_data

    def test_get_month_revenu_with_none_presta_selling_price(self):
        now = datetime.datetime.now()
        now_date = now.date()
        self.month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.months_data.create(date=self.month_date)
        presta1 = Prestation(date=now_date)
        presta2 = Prestation(date=now_date, selling_price=float(16))
        self.session.add(presta1)
        self.session.add(presta2)
        self.session.flush()
        month = self.biz.get.month(date=self.month_date, compute=True)
        self.assertEqual(month.revenu, float(16))
