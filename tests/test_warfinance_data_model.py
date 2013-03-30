 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine

import warbase.model

from warfinance.data.model import PrestationCost, Month, Prestation, Salesman
from . import TestData


class TestModelBase(TestData):

    def test_prestation_cost(self):
        user = PrestationCost.PrestationCost()
        self.assertTrue(True)

    def test_month(self):
        user = Month.Month()
        self.assertTrue(True)

    def test_prestation(self):
        user = Prestation.Prestation()
        self.assertTrue(True)

    def test_salesman(self):
        user = Salesman.Salesman()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
