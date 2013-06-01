 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine

import mozbase.model

from mozfinance.data.model import PrestationCost, Month, Prestation, Salesman
from . import TestData


class TestModelBase(TestData):

    def test_prestation_cost(self):
        PrestationCost.PrestationCost()
        self.assertTrue(True)

    def test_month(self):
        Month.Month()
        self.assertTrue(True)

    def test_prestation(self):
        Prestation.Prestation()
        self.assertTrue(True)

    def test_salesman(self):
        Salesman.Salesman()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
