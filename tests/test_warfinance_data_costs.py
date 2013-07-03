 # -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from mozfinance.data.cost import CostPrestationData
from mozfinance.data.model import *
from . import TestData


class TestCostsData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.pcost_data = CostPrestationData(
            package='mozfinance.data.model',
            dbsession=self.dbsession)

    def tearDown(self):
        TestData.tearDown(self)
        del self.pcost_data


class TestCreateCost(TestCostsData):

    def test_minimal_create(self):
        reason = u'Achat de traôneau'
        cost = self.pcost_data.create(
            reason=reason,
            prestation=self.prestation)
        self.assertTrue(isinstance(cost, CostPrestation.CostPrestation))
        self.assertEqual(reason, cost.reason)
        self.assertEqual(cost.prestation, self.prestation)

    def test_wrong_reason(self):
        with self.assertRaises(MultipleInvalid):
            self.pcost_data.create(
                reason='Not unicode',
                prestation=self.prestation)

    def test_wrong_amount(self):
        with self.assertRaises(MultipleInvalid):
            self.pcost_data.create(
                amount=12,
                prestation=self.prestation)


class TestUpdateCost(TestCostsData):

    def test_update(self):
        cost = self.pcost_data.create(
            reason=u'With action',
            prestation=self.prestation)
        cost = self.pcost_data.update(
            cost=cost,
            amount=float(12))
        self.assertEqual(cost.amount, float(12))

    def test_update_with_cost_id(self):
        cost = self.pcost_data.create(
            reason=u'With action',
            prestation=self.prestation)
        cost = self.pcost_data.update(
            cost_id=cost.id,
            amount=float(12))
        self.assertEqual(cost.amount, float(12))

    def test_no_update(self):
        reason = u'With action'
        cost = self.pcost_data.create(
            reason=reason,
            amount=float(12),
            prestation=self.prestation)
        self.assertTrue(not self.pcost_data.update(
            cost=cost,
            reason=reason,
            amount=float(12)))
        self.assertTrue(not self.pcost_data.update(
            cost=cost,
            amount=float(12)))
        self.assertTrue(not self.pcost_data.update(
            cost=cost,
            reason=reason))

    def test_wrong_update(self):
        cost = self.pcost_data.create(
            reason=u'With action',
            prestation=self.prestation)
        with self.assertRaises(MultipleInvalid):
            self.pcost_data.update(
                cost=cost,
                amount=13)

    def test_wrong_cost_on_update(self):
        with self.assertRaises(AttributeError):
            self.pcost_data.update(
                cost='cost',
                amount=13.0)

    def test_no_cost_on_update(self):
        with self.assertRaises(TypeError):
            self.pcost_data.update(
                amount=13.0)


class TestRemoveCost(TestCostsData):

    def test_remove_cost(self):
        cost = self.pcost_data.create(
            reason=u'With action',
            prestation=self.prestation)
        cost = self.pcost_data.remove(
            cost=cost)
        with self.assertRaises(NoResultFound):
            self.dbsession.query(CostPrestation.CostPrestation).one()


if __name__ == '__main__':
    unittest.main()
