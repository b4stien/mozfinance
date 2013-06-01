# -*- coding: utf-8 -*-
import unittest
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import mozbase.model
from mozbase.model import *
from mozbase.data.user import UserData

from mozfinance.data.model import *


class TestData(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        mozbase.model.Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.dbsession = Session()

        self.user_data = UserData(dbsession=self.dbsession)
        self.user = self.user_data.create(
            login='bastien', mail='bastien@test')

        now = datetime.datetime.now().date()
        self.prestation = Prestation.Prestation(date=now)
        self.dbsession.add(self.prestation)
        self.dbsession.flush()

    def tearDown(self):
        self.dbsession.close()
        mozbase.model.Base.metadata.drop_all(self.engine)
        del self.dbsession
        del self.user_data
        del self.user
        del self.prestation
