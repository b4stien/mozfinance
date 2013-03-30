 # -*- coding: utf-8 -*-
import datetime

from warfinance.data.model.Month import Month
from warfinance.data.months import MonthsData
from warfinance.biz import BusinessWorker

from . import TestData


class TestBusiness(TestData):

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


class TestBusinessBase(TestBusiness):

    def test_get_none_value(self):
        now = datetime.datetime.now()
        month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.months_data.create(date=month_date)
        month = self.biz.get.month(date=month_date)
        self.assertEqual(month.revenu, None)
        self.assertEqual(month.total_cost, None)
        self.assertEqual(month.gross_margin, None)

    def test_get_computed_values(self):
        now = datetime.datetime.now()
        month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.months_data.create(date=month_date)
        month = self.biz.get.month(date=month_date, compute=True)
        self.assertEqual(month.revenu, 0)
        self.assertEqual(month.total_cost, 0)
        self.assertEqual(month.gross_margin, 0)

    def test_get_stored_computed_values(self):
        now = datetime.datetime.now()
        month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.months_data.create(date=month_date)
        month = self.biz.get.month(date=month_date, compute=True)
        other_month = self.biz.get.month(date=month_date)
        self.assertEqual(other_month.revenu, 0)
        self.assertEqual(other_month.total_cost, 0)
        self.assertEqual(other_month.gross_margin, 0)

    def test_get_month_with_create(self):
        now = datetime.datetime.now()
        month_date = datetime.date(year=now.year, month=now.month, day=1)
        month = self.biz.get.month(date=month_date, create=True)
        self.assertTrue(isinstance(month, Month))

    def test_get_month_with_raw_date(self):
        now = datetime.datetime.now()
        month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.months_data.create(date=month_date)
        month = self.biz.get.month(date=now.date())
        self.assertTrue(isinstance(month, Month))

    def test_get_month_with_wrong_date(self):
        with self.assertRaises(AttributeError):
            month = self.biz.get.month(date='now.date()')
