 # -*- coding: utf-8 -*-
import datetime

from mozfinance.data.model.Prestation import Prestation

from . import TestData


class TestBusinessExpire(TestData):

    def setUp(self):
        TestData.setUp(self)

    def tearDown(self):
        TestData.tearDown(self)

    def test_prestation_expire(self):
        a_date = datetime.date(year=2012, month=5, day=27)
        presta = Prestation(date=a_date)
        self.dbsession.add(presta)
        self.dbsession.commit()
        presta = self.biz.prestation.set_selling_price(
            prestation=presta,
            selling_price=float(13))
        p1 = self.biz.prestation.get(prestation=presta, compute=True)
        self.assertEqual(p1.margin, float(13))
        p1 = self.biz.prestation.set_selling_price(
            prestation=p1,
            selling_price=float(17))
        p2 = self.biz.prestation.get(prestation=p1, compute=True)
        self.assertEqual(p2.margin, float(17))
