 # -*- coding: utf-8 -*-
import datetime

from warfinance.biz import BusinessWorker
from warfinance.data.model.Prestation import Prestation

from . import TestData


class TestBusinessExpire(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.biz = BusinessWorker(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        del self.biz

    def test_prestation_expire(self):
        now = datetime.datetime.now()
        now_date = now.date()
        presta = Prestation(date=now_date)
        self.session.add(presta)
        self.session.commit()
        presta = self.biz.data.prestations.set_selling_price(
            prestation=presta,
            selling_price=float(13))
        p1 = self.biz.get.prestation(prestation=presta, compute=True)
        self.assertEqual(p1.margin, float(13))
        p1 = self.biz.data.prestations.set_selling_price(
            prestation=p1,
            selling_price=float(17))
        p2 = self.biz.get.prestation(prestation=p1, compute=True)
        self.assertEqual(p2.margin, float(17))
