# -*- coding: utf-8 -*-
import unittest
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dogpile.cache import make_region

import mozbase.model
from mozbase.model import *
from mozbase.data.user import UserData
from mozbase.util.database import transaction

from mozfinance.data.model import *
from mozfinance.biz import BusinessWorker


class TestData(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        mozbase.model.Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.dbsession = Session()

        cache_region = make_region().configure('dogpile.cache.memory')
        setattr(self.dbsession, 'cache', cache_region)

        self.user_data = UserData(dbsession=self.dbsession)
        self.user = self.user_data.create(
            login='bastien', mail='bastien@test')

        a_date = datetime.date(year=2012, month=5, day=26)
        self.prestation = Prestation.Prestation(date=a_date)
        self.dbsession.add(self.prestation)
        self.dbsession.flush()

        self.biz = BusinessWorker(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user)

        with transaction(self.dbsession):
            for i in range(12):
                da_date = datetime.date(year=2012, month=i+1, day=1)
                self.biz.month.create(date=da_date)



    def tearDown(self):
        self.dbsession.close()
        mozbase.model.Base.metadata.drop_all(self.engine)
        del self.dbsession
        del self.user_data
        del self.user
        del self.prestation
