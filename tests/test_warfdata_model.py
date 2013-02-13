 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine

import warbmodel

from warfdata.model import Action, Cost, Month, Prestation, Salesman


class TestModelBase(unittest.TestCase):

    def test_action(self):
        application = Action.Action()
        self.assertTrue(True)

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


class TestModelCreateAll(unittest.TestCase):

    def test_create_all(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        warbmodel.Base.metadata.create_all(engine)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
