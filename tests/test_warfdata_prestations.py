 # -*- coding: utf-8 -*-
from datetime import date

from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from warbmodel import *

from warfdata.prestations import PrestationsData
from warfdata.model import *
from . import TestData


class TestMonthsData(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.presta_data = PrestationsData(
            application=self.app,
            package='warfdata.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        del self.presta_data

    def test_correct_update(self):
        pass


if __name__ == '__main__':
    unittest.main()
