# -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import warbase.model
from warbase.model import *
from warbase.data.users import UsersData
from warbase.data.applications import ApplicationsData

from warfinance.data.model import *
from warfinance.data.costs import CostsData


class TestData(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        warbase.model.Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.users_data = UsersData(session=self.session)
        self.user = self.users_data.create(
            login='bastien', mail='bastien@test')

        self.apps_data = ApplicationsData(session=self.session)
        self.app = self.apps_data.create(
            name='wartest',
            url='http://test/',
            min_permission='view',
            title='Tests')

        self.prestation = Prestation.Prestation()

    def tearDown(self):
        self.session.close()
        warbase.model.Base.metadata.drop_all(self.engine)
        del self.session
        del self.users_data
        del self.user
        del self.apps_data
        del self.app
        del self.prestation
