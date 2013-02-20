 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine

import warbmodel

from warfdata.model import Cost, Month, Prestation, Salesman
from . import TestData


class TestModelBase(TestData):

    def test_cost(self):
        user = Cost.Cost()
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
