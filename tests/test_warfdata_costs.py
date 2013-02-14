 # -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from warbmodel import *

from warfdata.model import *
from . import TestDatas


class TestCreateCost(TestDatas):

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


class TestUpdateCost(TestDatas):

    def test_update(self):
        cost = self.costs_data.create(
            reason=u'With action',
            prestation=self.prestation)
        cost = self.costs_data.update(
            cost=cost,
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


if __name__ == '__main__':
    unittest.main()
