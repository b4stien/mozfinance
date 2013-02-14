 # -*- coding: utf-8 -*-
from datetime import date

from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from warbmodel import *

from warfdata.prestations import PrestationsData
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

    def test_correct_update(self):
        self.prestation = self.presta_data.set_selling_price(
            prestation=self.prestation,
            selling_price=float(12))
        self.assertEqual(self.prestation.selling_price, float(12))
        with self.assertRaises(NoResultFound):
            self.session.query(Action.Action).one()

    def test_correct_update_with_action(self):
        self.prestation = self.presta_data.set_selling_price(
            prestation_id=self.prestation.id,
            selling_price=float(12),
            pop_action=True)
        self.session.query(Action.Action).one()

    def test_wrong_update(self):
        with self.assertRaises(AttributeError):
            self.prestation = self.presta_data.set_selling_price(
                prestation_id=self.prestation.id,
                selling_price=12,
                pop_action=True)
        with self.assertRaises(NoResultFound):
            self.session.query(Action.Action).one()


if __name__ == '__main__':
    unittest.main()
