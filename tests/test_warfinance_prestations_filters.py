# -*- coding: utf-8 -*-
import unittest
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dogpile.cache import make_region

import mozbase.model
from mozbase.model import *
from mozbase.data.user import UserData

from mozfinance.data.model import *

import mozfinance
from mozfinance.biz import BusinessWorker


class TestPrestationsFilter(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        mozbase.model.Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.dbsession = Session()

        cache_region = make_region().configure('dogpile.cache.memory')
        setattr(self.dbsession, 'cache', cache_region)

        self.users_data = UserData(dbsession=self.dbsession)
        self.user = self.users_data.create(
            login='bastien', mail='bastien@test')

        self.biz = BusinessWorker(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user)

    def tearDown(self):
        self.dbsession.close()
        mozbase.model.Base.metadata.drop_all(self.engine)
        mozfinance.PRESTATIONS_FILTERS = []
        del self.dbsession
        del self.users_data
        del self.user

    def test_basic_filter(self):
        # Dumb filter
        mozfinance.PRESTATIONS_FILTERS.append(Prestation.Prestation.id == 1)

        now = datetime.datetime.now()
        now_date = now.date()
        month_date = datetime.date(year=now.year, month=now.month, day=1)

        self.biz.month.create(
            date=month_date,
            cost=float(2000))

        presta = Prestation.Prestation(
            date=now_date,
            selling_price=float(4000),
            category=0,
            sector=0)
        self.dbsession.add(presta)
        self.dbsession.commit()

        presta_two = Prestation.Prestation(
            date=now_date,
            selling_price=float(8000),
            category=0,
            sector=0)
        self.dbsession.add(presta_two)
        self.dbsession.commit()

        month = self.biz.month.get(date=month_date, compute=True)

        self.assertEqual(month.gross_margin, float(4000))
