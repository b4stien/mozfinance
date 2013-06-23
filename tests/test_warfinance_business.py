 # -*- coding: utf-8 -*-
import datetime

from mozfinance.data.model.Month import Month
from mozfinance.data.month import MonthData
from mozfinance.biz import BusinessWorker

from . import TestData


class TestBusiness(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.biz = BusinessWorker(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user)
        self.month_data = MonthData(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        del self.biz
        del self.month_data


class TestBusinessBase(TestBusiness):

    def test_get_none_value(self):
        now = datetime.datetime.now()
        month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.month_data.create(date=month_date)
        month = self.biz.month.get(date=month_date)
        self.assertEqual(month.revenue, float(0))
        self.assertEqual(month.total_prestation_cost, float(0))
        self.assertEqual(month.gross_margin, float(0))

    def test_get_computed_values(self):
        now = datetime.datetime.now()
        month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.month_data.create(date=month_date)
        month = self.biz.month.get(date=month_date, compute=True)
        self.assertEqual(month.revenue, 0)
        self.assertEqual(month.total_prestation_cost, 0)
        self.assertEqual(month.gross_margin, 0)

    def test_get_stored_computed_values(self):
        month_date = datetime.date(year=2012, month=5, day=1)
        month = self.biz.month.get(date=month_date)
        self.assertEqual(month.revenue, float(0))

        other_test = self.biz.month._dbsession.cache.get(
            key='month:{}:revenue'.format(month.id))
        self.assertEqual(other_test, float(0))

        other_month = self.biz.month.get(date=month_date)
        self.assertEqual(other_month.revenue, 0)
        self.assertEqual(other_month.total_prestation_cost, 0)
        self.assertEqual(other_month.gross_margin, 0)

    def test_get_month_with_raw_date(self):
        now = datetime.datetime.now()
        month_date = datetime.date(year=now.year, month=now.month, day=1)
        self.month_data.create(date=month_date)
        month = self.biz.month.get(date=now.date())
        self.assertTrue(isinstance(month, Month))

    def test_get_month_with_wrong_date(self):
        with self.assertRaises(AttributeError):
            self.biz.month.get(date='now.date()')
