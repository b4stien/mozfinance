 # -*- coding: utf-8 -*-
from datetime import date

from voluptuous import MultipleInvalid

from mozfinance.data.month import MonthData
from mozfinance.data.model import *
from . import TestData


class TestMonthsData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.month_data = self.biz.month

    def tearDown(self):
        TestData.tearDown(self)
        del self.month_data


class TestCreateMonth(TestMonthsData):

    def test_minimal_create(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.month_data.get(
            date=month_date)
        self.assertTrue(isinstance(month, Month.Month))
        self.assertEqual(month.date, month_date)

        other_month = self.month_data.get(month.id)
        self.assertEqual(other_month, month)

    def test_wrong_date(self):
        with self.assertRaises(MultipleInvalid):
            self.month_data.create(
                date='foo')
        with self.assertRaises(MultipleInvalid):
            self.month_data.create(
                date=date(year=2008, month=10, day=14))


class TestUpdateMonth(TestMonthsData):

    def test_basique(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.month_data.get(
            date=month_date)
        self.assertEqual(month.date, month_date)
        with self.assertRaises(NotImplementedError):
            self.month_data.update(
                month=month,
                cost=float(27000))


class TestRemoveMonth(TestMonthsData):
    def test_basique(self):
        month = self.month_data.get(date=date(year=2012, month=12, day=1))
        with self.assertRaises(NotImplementedError):
            self.month_data.remove(month=month)


if __name__ == '__main__':
    unittest.main()
