 # -*- coding: utf-8 -*-
from datetime import date

from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from warbmodel import *

from warfdata.prestations import PrestationsData
from warfdata.salesmen import SalesmenData
from warfdata.model import *
from . import TestData


class TestPrestationsData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.presta_data = PrestationsData(
            application=self.app,
            package='warfdata.model',
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
            application=self.app,
            package='warfdata.model',
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
            application=self.app,
            package='warfdata.model',
            session=self.session,
            user=self.user)

    def test_set_correct_custom_formula(self):
        pass


if __name__ == '__main__':
    unittest.main()
