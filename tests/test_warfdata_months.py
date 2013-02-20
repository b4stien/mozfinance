 # -*- coding: utf-8 -*-
from datetime import date

from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from warbmodel import *

from warfdata.months import MonthsData
from warfdata.model import *
from . import TestData


class TestMonthsData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.months_data = MonthsData(
            application=self.app,
            package='warfdata.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        del self.months_data


class TestCreateMonth(TestMonthsData):

    def test_minimal_create(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.months_data.create(
            date=month_date)
        self.assertTrue(isinstance(month, Month.Month))
        self.assertEqual(month.date, month_date)
        with self.assertRaises(NoResultFound):
            self.session.query(Action.Action).one()

    def test_wrong_date(self):
        with self.assertRaises(MultipleInvalid):
            month = self.months_data.create(
                date='foo')
        with self.assertRaises(MultipleInvalid):
            month = self.months_data.create(
                date=date(year=2008, month=10, day=14))

    def test_complete_create(self):
        month_date = date(year=2008, month=7, day=1)
        month = self.months_data.create(
            date=month_date,
            breakeven=float(27000))
        self.assertEqual(month.date, month_date)
        self.assertEqual(month.breakeven, float(27000))


class TestUpdateMonth(TestMonthsData):

    def test_correct_update(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.months_data.create(
            date=month_date)
        self.assertEqual(month.date, month_date)
        month = self.months_data.update(
            month=month,
            breakeven=float(27000))
        self.assertEqual(month.date, month_date)
        self.assertEqual(month.breakeven, float(27000))

    def test_update_with_date(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.months_data.create(
            date=month_date)
        month = self.months_data.update(
            date=month_date,
            breakeven=float(27000))
        self.assertEqual(month.breakeven, float(27000))

    def test_update_with_month_id(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.months_data.create(
            date=month_date)
        month = self.months_data.update(
            month_id=month.id,
            breakeven=float(27000))
        self.assertEqual(month.breakeven, float(27000))

    def test_update_with_action(self):
        month = self.months_data.create(date=date(year=2012, month=12, day=1))
        month = self.months_data.update(
            month=month,
            breakeven=float(27000),
            pop_action=True)
        action = self.session.query(Action.Action).one()

    def test_correct_noupdate(self):
        month_date = date(year=2012, month=12, day=1)
        month = self.months_data.create(
            date=month_date,
            breakeven=float(27000))
        month = self.months_data.update(
            month=month,
            breakeven=float(27000),
            pop_action=False)
        self.assertTrue(not month)

    def test_wrong_month(self):
        with self.assertRaises(AttributeError):
            month = self.months_data.update(
                month='month',
                breakeven=float(27000),
                pop_action=False)

    def test_wrong_date(self):
        with self.assertRaises(AttributeError):
            month = self.months_data.update(
                date='month',
                breakeven=float(27000),
                pop_action=False)

    def test_wrong_info(self):
        with self.assertRaises(TypeError):
            month = self.months_data.update(
                breakeven=float(27000),
                pop_action=False)


class TestRemoveMonth(TestMonthsData):
    def test_basique(self):
        month = self.months_data.create(date=date(year=2012, month=12, day=1))
        with self.assertRaises(NotImplementedError):
            self.months_data.remove(
                month=month,
                pop_action=False)


if __name__ == '__main__':
    unittest.main()
