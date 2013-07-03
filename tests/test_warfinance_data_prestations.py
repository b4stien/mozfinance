 # -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound

from mozfinance.data.prestation import PrestationData
from mozfinance.data.salesman import SalesmanData
from mozfinance.data.model import *
from . import TestData


class TestPrestationsData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.presta_data = PrestationData(
            package='mozfinance.data.model',
            dbsession=self.dbsession)

    def tearDown(self):
        TestData.tearDown(self)
        del self.presta_data


class TestPrestationsBase(TestPrestationsData):

    def test_correct_update(self):
        self.prestation = self.presta_data.set_selling_price(
            prestation=self.prestation,
            selling_price=float(12))
        self.assertEqual(self.prestation.selling_price, float(12))

    def test_no_update(self):
        self.prestation = self.presta_data.set_selling_price(
            prestation=self.prestation,
            selling_price=float(12))
        self.prestation = self.presta_data.set_selling_price(
            prestation=self.prestation,
            selling_price=float(12))
        self.assertTrue(not self.prestation)

    def test_wrong_selling_price(self):
        with self.assertRaises(AttributeError):
            self.prestation = self.presta_data.set_selling_price(
                prestation_id=self.prestation.id,
                selling_price=12)

    def test_wrong_prestation(self):
        with self.assertRaises(AttributeError):
            self.prestation = self.presta_data.set_selling_price(
                prestation='self.prestation.id',
                selling_price=12)

    def test_wrong_info(self):
        with self.assertRaises(TypeError):
            self.prestation = self.presta_data.set_selling_price(
                selling_price=12)

    def test_no_selling_price(self):
        with self.assertRaises(TypeError):
            self.prestation = self.presta_data.set_selling_price(
                prestation_id=self.prestation.id)


class TestPrestationsSalesmen(TestPrestationsData):

    def setUp(self):
        TestPrestationsData.setUp(self)
        self.salesmen_data = SalesmanData(
            package='mozfinance.data.model',
            dbsession=self.dbsession)
        self.salesman = self.salesmen_data.create(
            firstname=u'Johny',
            lastname=u'Doe')
        com_form = {}
        com_form[0] = {}
        com_form[0][0] = 'bla'
        self.salesmen_data.set_commissions_formulae(
            salesman=self.salesman,
            commissions_formulae=com_form)

    def test_correct_add_salesman(self):
        self.presta_data.add_salesman(
            prestation=self.prestation,
            salesman=self.salesman)
        presta_sm = self.presta_data._get.prestation_salesman(
            salesman=self.salesman,
            prestation=self.prestation)
        self.assertEqual(presta_sm.formula, 'bla')

    def test_readd_salesman(self):
        self.presta_data.add_salesman(
            prestation=self.prestation,
            salesman=self.salesman)
        a_bool = self.presta_data.add_salesman(
            prestation=self.prestation,
            salesman=self.salesman)
        self.assertTrue(not a_bool)

    def test_correct_remove_salesman(self):
        self.presta_data.add_salesman(
            prestation=self.prestation,
            salesman=self.salesman)
        self.presta_data.remove_salesman(
            prestation=self.prestation,
            salesman=self.salesman)
        self.assertEqual([], self.prestation.salesmen)

    def test_remove_non_salesman(self):
        presta = self.presta_data.remove_salesman(
            prestation=self.prestation,
            salesman=self.salesman)
        self.assertEqual(presta, self.prestation)

    def test_correct_delete_salesman(self):
        self.presta_data.add_salesman(
            prestation=self.prestation,
            salesman=self.salesman)
        self.salesmen_data.remove(salesman=self.salesman)
        with self.assertRaises(NoResultFound):
            self.dbsession.query(AssPrestationSalesman.PrestationSalesman).one()

    def test_correct_delete_prestation(self):
        self.presta_data.add_salesman(
            prestation=self.prestation,
            salesman=self.salesman)

        # Prestation create/remove not handle by warfinance.data.prestations
        self.dbsession.delete(self.prestation)
        self.dbsession.commit()

        with self.assertRaises(NoResultFound):
            self.dbsession.query(AssPrestationSalesman.PrestationSalesman).one()


class TestFormulae(TestPrestationsData):

    def setUp(self):
        TestPrestationsData.setUp(self)
        self.salesmen_data = SalesmanData(
            package='mozfinance.data.model',
            dbsession=self.dbsession)
        self.salesman = self.salesmen_data.create(
            firstname=u'Robert',
            lastname=u'Louis')
        com_form = {}
        com_form[0] = {}
        com_form[0][0] = 'bla'
        self.salesmen_data.set_commissions_formulae(
            salesman=self.salesman,
            commissions_formulae=com_form)
        self.presta_data.add_salesman(
            salesman=self.salesman,
            prestation=self.prestation)

    def test_set_correct_formula(self):
        self.presta_data.set_salesman_formula(
            salesman=self.salesman,
            prestation=self.prestation,
            formula='lol')
        presta_sm = self.presta_data._get.prestation_salesman(
            salesman=self.salesman,
            prestation=self.prestation)
        self.assertEqual(presta_sm.formula, 'lol')

    def test_wrong_custom_formula(self):
        with self.assertRaises(AttributeError):
            self.presta_data.set_salesman_formula(
                salesman=self.salesman,
                prestation=self.prestation,
                formula=u'lol')

    def test_no_update_set_custom_formula(self):
        self.presta_data.set_salesman_formula(
            salesman=self.salesman,
            prestation=self.prestation,
            formula='lol')
        a_bool = self.presta_data.set_salesman_formula(
            salesman=self.salesman,
            prestation=self.prestation,
            formula='lol')
        self.assertTrue(not a_bool)

    def test_backup_default_formula(self):
        # Default formula
        presta_sm = self.presta_data._get.prestation_salesman(
            salesman=self.salesman,
            prestation=self.prestation)
        self.assertEqual(presta_sm.formula, 'bla')
        # We change the formula
        self.presta_data.set_salesman_formula(
            salesman=self.salesman,
            prestation=self.prestation,
            formula='lol')
        presta_sm = self.presta_data._get.prestation_salesman(
            salesman=self.salesman,
            prestation=self.prestation)
        self.assertEqual(presta_sm.formula, 'lol')
        # And we go back to default
        self.presta_data.set_salesman_formula(
            salesman=self.salesman,
            prestation=self.prestation,
            formula=None)
        presta_sm = self.presta_data._get.prestation_salesman(
            salesman=self.salesman,
            prestation=self.prestation)
        self.assertEqual(presta_sm.formula, 'bla')


class TestRatios(TestPrestationsData):

    def setUp(self):
        TestPrestationsData.setUp(self)
        self.salesmen_data = SalesmanData(
            package='mozfinance.data.model',
            dbsession=self.dbsession)
        self.salesman = self.salesmen_data.create(
            firstname=u'Robert',
            lastname=u'Louis')
        com_form = {}
        com_form[0] = {}
        com_form[0][0] = 'bla'
        self.salesmen_data.set_commissions_formulae(
            salesman=self.salesman,
            commissions_formulae=com_form)
        self.presta_data.add_salesman(
            salesman=self.salesman,
            prestation=self.prestation)

    def test_set_correct_ratio(self):
        self.presta_data.set_salesman_ratio(
            salesman=self.salesman,
            prestation=self.prestation,
            ratio=float(0.3))
        presta_sm = self.presta_data._get.prestation_salesman(
            salesman=self.salesman,
            prestation=self.prestation)
        self.assertEqual(presta_sm.ratio, float(0.3))

    def test_update_ratio(self):
        self.presta_data.set_salesman_ratio(
            salesman=self.salesman,
            prestation=self.prestation,
            ratio=float(0.3))
        self.presta_data.set_salesman_ratio(
            salesman=self.salesman,
            prestation=self.prestation,
            ratio=float(0.8))
        presta_sm = self.presta_data._get.prestation_salesman(
            salesman=self.salesman,
            prestation=self.prestation)
        self.assertEqual(presta_sm.ratio, float(0.8))

    def test_remove_ratio(self):
        self.presta_data.set_salesman_ratio(
            salesman=self.salesman,
            prestation=self.prestation,
            ratio=float(0.3))
        self.presta_data.set_salesman_ratio(
            salesman=self.salesman,
            prestation=self.prestation,
            ratio=None)
        presta_sm = self.presta_data._get.prestation_salesman(
            salesman=self.salesman,
            prestation=self.prestation)
        self.assertTrue(presta_sm.ratio is None)

    def test_wrong_ratio(self):
        with self.assertRaises(AttributeError):
            self.presta_data.set_salesman_ratio(
                salesman=self.salesman,
                prestation=self.prestation,
                ratio=u'lol')

    def test_no_update_set_custom_ratios(self):
        self.presta_data.set_salesman_ratio(
            salesman=self.salesman,
            prestation=self.prestation,
            ratio=float(0.3))
        a_bool = self.presta_data.set_salesman_ratio(
            salesman=self.salesman,
            prestation=self.prestation,
            ratio=float(0.3))
        self.assertTrue(not a_bool)


if __name__ == '__main__':
    unittest.main()
