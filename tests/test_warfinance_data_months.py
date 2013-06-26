 # -*- coding: utf-8 -*-
from datetime import date

from voluptuous import MultipleInvalid

from mozfinance.data.month import MonthData
from mozfinance.data.model import *
from . import TestData


class TestMonthsData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.month_data = MonthData(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user)

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

    def test_wrong_date(self):
        with self.assertRaises(MultipleInvalid):
            self.month_data.create(
                date='foo')
        with self.assertRaises(MultipleInvalid):
            self.month_data.create(
                date=date(year=2008, month=10, day=14))

    def test_complete_create(self):
        month_date = date(year=2011, month=1, day=1)
        month = self.month_data.create(
            date=month_date,
            cost=float(27000))
        self.assertEqual(month.date, month_date)
        self.assertEqual(month.cost, float(27000))


class TestUpdateMonth(TestMonthsData):

    def test_correct_update(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.month_data.get(
            date=month_date)
        self.assertEqual(month.date, month_date)
        month = self.month_data.update(
            month=month,
            cost=float(27000))
        self.assertEqual(month.date, month_date)
        self.assertEqual(month.cost, float(27000))

    def test_update_with_date(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.month_data.get(
            date=month_date)
        month = self.month_data.update(
            date=month_date,
            cost=float(27000))
        self.assertEqual(month.cost, float(27000))

    def test_update_with_month_id(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.month_data.get(
            date=month_date)
        month = self.month_data.update(
            month_id=month.id,
            cost=float(27000))
        self.assertEqual(month.cost, float(27000))

    def test_correct_noupdate(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.month_data.update(
            date=month_date,
            cost=float(27000))
        month = self.month_data.update(
            month=month,
            cost=float(27000))
        self.assertTrue(not month)

    def test_wrong_month(self):
        with self.assertRaises(AttributeError):
            self.month_data.update(
                month='month',
                cost=float(27000))

    def test_wrong_date(self):
        with self.assertRaises(AttributeError):
            self.month_data.update(
                date='month',
                cost=float(27000))

    def test_wrong_info(self):
        with self.assertRaises(TypeError):
            self.month_data.update(
                cost=float(27000))


class TestRemoveMonth(TestMonthsData):
    def test_basique(self):
        month = self.month_data.get(date=date(year=2012, month=12, day=1))
        with self.assertRaises(NotImplementedError):
            self.month_data.remove(month=month)


if __name__ == '__main__':
    unittest.main()
