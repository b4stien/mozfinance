# -*- coding: utf-8 -*-
import unittest
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import warbase.model
from warbase.model import *
from warbase.data.users import UsersData

from warfinance.data.model import *

import warfinance
from warfinance.biz import BusinessWorker


class TestPrestationsFilter(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        warbase.model.Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.users_data = UsersData(session=self.session)
        self.user = self.users_data.create(
            login='bastien', mail='bastien@test')

        self.biz = BusinessWorker(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        self.session.close()
        warbase.model.Base.metadata.drop_all(self.engine)
        warfinance.PRESTATIONS_FILTERS = []
        del self.session
        del self.users_data
        del self.user

    def test_basic_filter(self):
        # Dumb filter
        warfinance.PRESTATIONS_FILTERS.append(Prestation.Prestation.id == 1)

        now = datetime.datetime.now()
        now_date = now.date()
        month_date = datetime.date(year=now.year, month=now.month, day=1)

        self.biz.data.months.create(
            date=month_date,
            cost=float(2000))

        presta = Prestation.Prestation(
            date=now_date,
            selling_price=float(4000),
            category=0,
            sector=0)
        self.session.add(presta)
        self.session.commit()

        presta_two = Prestation.Prestation(
            date=now_date,
            selling_price=float(8000),
            category=0,
            sector=0)
        self.session.add(presta_two)
        self.session.commit()

        month = self.biz.get.month(date=month_date, compute=True)

        self.assertEqual(month.gross_margin, float(4000))

    def test_complete_filter(self):
        pass
