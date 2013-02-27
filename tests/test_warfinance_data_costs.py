 # -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from warbase.model import *

from warfinance.data.costs import CostsData
from warfinance.data.model import *
from . import TestData


class TestCostsData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.costs_data = CostsData(
            application=self.app,
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        del self.costs_data


class TestCreateCost(TestCostsData):

    def test_minimal_create(self):
        reason = u'Achat de traôneau'
        cost = self.costs_data.create(
            reason=reason,
            prestation=self.prestation,
            pop_action=False)
        self.assertTrue(isinstance(cost, Cost.Cost))
        self.assertEqual(reason, cost.reason)
        self.assertEqual(cost.prestation, self.prestation)
        with self.assertRaises(NoResultFound):
            self.session.query(Action.Action).one()

    def test_create_with_action(self):
        cost = self.costs_data.create(
            reason=u'With action',
            prestation=self.prestation,
            pop_action=True)
        action = self.session.query(Action.Action).one()

    def test_wrong_reason(self):
        with self.assertRaises(MultipleInvalid):
            cost = self.costs_data.create(
                reason='Not unicode',
                prestation=self.prestation,
                pop_action=True)
        with self.assertRaises(NoResultFound):
            action = self.session.query(Action.Action).one()

    def test_wrong_amount(self):
        with self.assertRaises(MultipleInvalid):
            cost = self.costs_data.create(
                amount=12,
                prestation=self.prestation,
                pop_action=True)
        with self.assertRaises(NoResultFound):
            action = self.session.query(Action.Action).one()


class TestUpdateCost(TestCostsData):

    def test_update(self):
        cost = self.costs_data.create(
            reason=u'With action',
            prestation=self.prestation)
        cost = self.costs_data.update(
            cost=cost,
            amount=float(12))
        self.assertEqual(cost.amount, float(12))

    def test_update_with_cost_id(self):
        cost = self.costs_data.create(
            reason=u'With action',
            prestation=self.prestation)
        cost = self.costs_data.update(
            cost_id=cost.id,
            amount=float(12))
        self.assertEqual(cost.amount, float(12))

    def test_no_update(self):
        reason = u'With action'
        cost = self.costs_data.create(
            reason=reason,
            amount=float(12),
            prestation=self.prestation)
        self.assertTrue(not self.costs_data.update(
            cost=cost,
            reason=reason,
            amount=float(12)))
        self.assertTrue(not self.costs_data.update(
            cost=cost,
            amount=float(12)))
        self.assertTrue(not self.costs_data.update(
            cost=cost,
            reason=reason))

    def test_wrong_update(self):
        cost = self.costs_data.create(
            reason=u'With action',
            prestation=self.prestation,
            pop_action=False)
        with self.assertRaises(MultipleInvalid):
            self.costs_data.update(
                cost=cost,
                amount=13,
                pop_action=True)
        with self.assertRaises(NoResultFound):
            action = self.session.query(Action.Action).one()

    def test_wrong_cost_on_update(self):
        with self.assertRaises(AttributeError):
            self.costs_data.update(
                cost='cost',
                amount=13.0,
                pop_action=True)

    def test_no_cost_on_update(self):
        with self.assertRaises(TypeError):
            self.costs_data.update(
                amount=13.0,
                pop_action=True)


class TestRemoveCost(TestCostsData):
    
    def test_remove_cost(self):
        cost = self.costs_data.create(
            reason=u'With action',
            prestation=self.prestation)
        cost = self.costs_data.remove(
            cost=cost)
        with self.assertRaises(NoResultFound):
            self.session.query(Cost.Cost).one()


if __name__ == '__main__':
    unittest.main()
