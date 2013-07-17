 # -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from mozfinance.data.salesman import SalesmanData
from mozfinance.data.model import *
from . import TestData


class TestSalesmenData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.salesmen_data = self.biz.salesman

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

    def test_wrong_create(self):
        with self.assertRaises(MultipleInvalid):
            self.salesmen_data.create(
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
            self.dbsession.query(Salesman.Salesman).one()

    def test_set_commissions_formulae(self):
        salesman = self.salesmen_data.create(
            firstname=u'Hubërt',
            lastname=u'Jean Claude Douze')
        self.salesmen_data.set_commissions_formulae(
            salesman=salesman,
            commissions_formulae={})
        self.salesmen_data.remove(
            salesman=salesman)

if __name__ == '__main__':
    unittest.main()
