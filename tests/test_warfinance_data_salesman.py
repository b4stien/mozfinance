 # -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from warbase.model import *

from warfinance.data.salesmen import SalesmenData
from warfinance.data.model import *
from . import TestData


class TestSalesmenData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.salesmen_data = SalesmenData(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        del self.salesmen_data

class TestGetSalesman(TestSalesmenData):

    def test_wrong_salesman(self):
        with self.assertRaises(AttributeError):
            self.salesmen_data.update(
                salesman='bla')

    def test_no_salesman(self):
        with self.assertRaises(TypeError):
            self.salesmen_data.update()

    def test_salesman_id(self):
        salesman = self.salesmen_data.create(
            firstname=u'Hubërt',
            lastname=u'Jean Claude Douze')
        salesman = self.salesmen_data.update(
            salesman_id=salesman.id,
            firstname=u'Douze')
        self.assertEqual(salesman.firstname, u'Douze')


class TestSalesmenBase(TestSalesmenData):

    def test_correct_create(self):
        salesman = self.salesmen_data.create(
            firstname=u'Hubërt',
            lastname=u'Jean Claude Douze')
        self.assertEqual(salesman.firstname, u'Hubërt')
        self.assertEqual(salesman.lastname, u'Jean Claude Douze')

    def test_correct_create_with_action(self):
        salesman = self.salesmen_data.create(
            firstname=u'Hubërt',
            lastname=u'Jean Claude Douze',
            pop_action=True)
        self.session.query(Action.Action).one()

    def test_wrong_create(self):
        with self.assertRaises(MultipleInvalid):
            salesman = self.salesmen_data.create(
                firstname='Hubërt',
                lastname=u'Jean Claude Douze')

    def test_correct_update(self):
        salesman = self.salesmen_data.create(
            firstname=u'Hubërt',
            lastname=u'Jean Claude Douze')
        salesman = self.salesmen_data.update(
            salesman=salesman,
            lastname=u'Jean-Louis')
        self.assertEqual(salesman.lastname, u'Jean-Louis')

    def test_correct_update_with_action(self):
        salesman = self.salesmen_data.create(
            firstname=u'Hubërt',
            lastname=u'Jean Claude Douze')
        salesman = self.salesmen_data.update(
            salesman=salesman,
            lastname=u'Jean-Louis',
            pop_action=True)
        self.session.query(Action.Action).one()

    def test_no_update(self):
        salesman = self.salesmen_data.create(
            firstname=u'Hubërt',
            lastname=u'Jean Claude Douze')
        salesman = self.salesmen_data.update(
            salesman=salesman,
            firstname=u'Hubërt')
        self.assertTrue(not salesman)

    def test_remove(self):
        salesman = self.salesmen_data.create(
            firstname=u'Hubërt',
            lastname=u'Jean Claude Douze')
        salesman = self.salesmen_data.remove(
            salesman=salesman)
        with self.assertRaises(NoResultFound):
            self.session.query(Salesman.Salesman).one()

    def test_remove_with_action(self):
        salesman = self.salesmen_data.create(
            firstname=u'Hubërt',
            lastname=u'Jean Claude Douze')
        salesman = self.salesmen_data.remove(
            salesman=salesman,
            pop_action=True)
        self.session.query(Action.Action).one()

if __name__ == '__main__':
    unittest.main()
