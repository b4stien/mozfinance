 # -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound

from warbase.model import *

from warfinance.data.prestations import PrestationsData
from warfinance.data.salesmen import SalesmenData
from warfinance.data.model import *
from . import TestData


class TestPrestationsData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.presta_data = PrestationsData(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)
        self.prestation = Prestation.Prestation()
        self.session.add(self.prestation)
        self.session.flush()

    def tearDown(self):
        TestData.tearDown(self)
        del self.presta_data


class TestPrestationsBase(TestPrestationsData):

    def test_correct_update(self):
        self.prestation = self.presta_data.set_selling_price(
            prestation=self.prestation,
            selling_price=float(12))
        self.assertEqual(self.prestation.selling_price, float(12))
        with self.assertRaises(NoResultFound):
            self.session.query(Action.Action).one()

    def test_no_update(self):
        self.prestation = self.presta_data.set_selling_price(
            prestation=self.prestation,
            selling_price=float(12))
        self.prestation = self.presta_data.set_selling_price(
            prestation=self.prestation,
            selling_price=float(12))
        self.assertTrue(not self.prestation)

    def test_correct_update_with_action(self):
        self.prestation = self.presta_data.set_selling_price(
            prestation_id=self.prestation.id,
            selling_price=float(12),
            pop_action=True)
        self.session.query(Action.Action).one()

    def test_wrong_selling_price(self):
        with self.assertRaises(AttributeError):
            self.prestation = self.presta_data.set_selling_price(
                prestation_id=self.prestation.id,
                selling_price=12,
                pop_action=True)
        with self.assertRaises(NoResultFound):
            self.session.query(Action.Action).one()

    def test_wrong_prestation(self):
        with self.assertRaises(AttributeError):
            self.prestation = self.presta_data.set_selling_price(
                prestation='self.prestation.id',
                selling_price=12,
                pop_action=True)

    def test_wrong_info(self):
        with self.assertRaises(TypeError):
            self.prestation = self.presta_data.set_selling_price(
                selling_price=12,
                pop_action=True)

    def test_no_selling_price(self):
        with self.assertRaises(TypeError):
            self.prestation = self.presta_data.set_selling_price(
                prestation_id=self.prestation.id,
                pop_action=True)


class TestPrestationsSalesmen(TestPrestationsData):

    def setUp(self):
        TestPrestationsData.setUp(self)
        self.salesmen_data = SalesmenData(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def test_correct_add_salesman(self):
        salesman = self.salesmen_data.create(
            firstname=u'Johny',
            lastname=u'Doe')
        self.prestation = self.presta_data.add_salesman(
            prestation=self.prestation,
            salesman=salesman,
            pop_action=True)

    def test_readd_salesman(self):
        salesman = self.salesmen_data.create(
            firstname=u'Johny',
            lastname=u'Doe')
        self.prestation = self.presta_data.add_salesman(
            prestation=self.prestation,
            salesman=salesman,
            pop_action=True)
        with self.assertRaises(Exception):
            self.prestation = self.presta_data.add_salesman(
                prestation=self.prestation,
                salesman=salesman,
                pop_action=True)

    def test_correct_remove_salesman(self):
        salesman = self.salesmen_data.create(
            firstname=u'Johny',
            lastname=u'Doe')
        self.prestation = self.presta_data.add_salesman(
            prestation=self.prestation,
            salesman=salesman,
            pop_action=True)
        self.prestation = self.presta_data.remove_salesman(
            prestation=self.prestation,
            salesman=salesman,
            pop_action=True)
        self.assertEqual([], self.prestation.salesmen)

    def test_remove_non_salesman(self):
        salesman = self.salesmen_data.create(
            firstname=u'Johny',
            lastname=u'Doe')
        with self.assertRaises(Exception):
            self.prestation = self.presta_data.remove_salesman(
                prestation=self.prestation,
                salesman=salesman,
                pop_action=True)


class TestCustomFormulae(TestPrestationsData):

    def setUp(self):
        TestPrestationsData.setUp(self)
        self.salesmen_data = SalesmenData(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)
        self.salesman = self.salesmen_data.create(
            firstname=u'Robert',
            lastname=u'Louis')
        self.prestation = self.presta_data.add_salesman(
            salesman=self.salesman,
            prestation=self.prestation)

    def test_set_correct_custom_formula(self):
        presta = self.presta_data.set_custom_com_formula(
            salesman=self.salesman,
            prestation=self.prestation,
            commission_formula='lol')
        self.assertTrue((self.salesman.id, 'lol') in presta.custom_com_formulae)

    def test_wrong_custom_formula(self):
        with self.assertRaises(AttributeError):
            presta = self.presta_data.set_custom_com_formula(
                salesman=self.salesman,
                prestation=self.prestation,
                commission_formula=u'lol')

    def test_no_update_set_custom_formula(self):
        presta = self.presta_data.set_custom_com_formula(
            salesman=self.salesman,
            prestation=self.prestation,
            commission_formula='lol')
        presta = self.presta_data.set_custom_com_formula(
            salesman=self.salesman,
            prestation=self.prestation,
            commission_formula='lol')
        self.assertTrue(not presta)

    def test_no_update_set_custom_formula(self):
        presta = self.presta_data.set_custom_com_formula(
            salesman=self.salesman,
            prestation=self.prestation,
            commission_formula='lol',
            pop_action=True)
        self.session.query(Action.Action).one()


if __name__ == '__main__':
    unittest.main()
