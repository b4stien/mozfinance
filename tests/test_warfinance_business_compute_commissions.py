# -*- coding: utf-8 -*-
import datetime

from mozfinance.data.model.Prestation import Prestation
import mozfinance

from . import TestData


class TestBusinessCompute(TestData):

    def setUp(self):
        TestData.setUp(self)

        def a_bonus(**kwargs):
            if kwargs['m_bc'] >= float(10000):
                return 0.01*kwargs['m_bc']

            return float(0)

        if not a_bonus in mozfinance.COMMISSIONS_BONUSES:
            mozfinance.COMMISSIONS_BONUSES.append(a_bonus)

    def tearDown(self):
        TestData.tearDown(self)
        mozfinance.COMMISSIONS_BONUSES = []

    def test_get_simple_commission(self):
        now = datetime.datetime.now()
        now_date = now.date()
        month_date = datetime.date(year=now.year, month=now.month, day=1)

        month = self.biz.month.create(date=month_date)
        self.biz.month.cost.create(month=month, amount=float(2000), reason=u'Noa')

        presta = Prestation(
            date=now_date,
            category=0,
            sector=0)
        self.dbsession.add(presta)
        self.dbsession.commit()

        self.biz.prestation.bill.create(prestation=presta, ref=u'Bla', amount=float(4000))

        salesman = self.biz.salesman.create(
            firstname=u'Bas',
            lastname=u'Gan')
        salesman = self.biz.salesman.set_commissions_formulae(
            salesman=salesman,
            commissions_formulae={0: {0: '{p_m}*{m_bc}/{m_mb}*0.06'}})

        self.biz.prestation.salesman.add(
            prestation=presta,
            salesman=salesman)

        self.biz.prestation.cost.create(
            prestation=presta,
            amount=float(100),
            reason=u'Auto Cost 1')

        commission_ideal = round(float(3900)*float(1900)/float(3900)*float(0.06), 1)

        sm = presta.prestation_salesmen[0]

        self.assertEqual(sm.formula, '{p_m}*{m_bc}/{m_mb}*0.06')
        self.assertEqual(sm.commission, commission_ideal)
        self.assertEqual(month.month_salesmen[0].commission_prestations, commission_ideal)

    def test_get_complexe_commission(self):
        month_date = datetime.date(year=2013, month=1, day=1)
        another_month_date = datetime.date(year=2013, month=2, day=1)

        month = self.biz.month.create(date=month_date)
        self.biz.month.create(date=another_month_date)

        self.biz.month.cost.create(month=month, amount=float(2000), reason=u'NoReson')
        self.biz.month.cost.create(month_date=another_month_date, amount=float(2000), reason=u'NoReson')

        presta = Prestation(
            date=month_date,
            category=0,
            sector=0)
        self.dbsession.add(presta)
        another_presta = Prestation(
            date=month_date,
            category=0,
            sector=0)
        self.dbsession.add(another_presta)
        another_month_presta = Prestation(
            date=another_month_date,
            category=0,
            sector=0)
        self.dbsession.add(another_month_presta)
        self.dbsession.commit()

        self.biz.prestation.bill.create(prestation=presta, ref=u'Bla', amount=float(25000))
        self.biz.prestation.bill.create(prestation=another_presta, ref=u'Bla', amount=float(25000))
        self.biz.prestation.bill.create(prestation=another_month_presta, ref=u'Bla', amount=float(25000))

        salesman = self.biz.salesman.create(
            firstname=u'Bas',
            lastname=u'Gan')
        salesman = self.biz.salesman.set_commissions_formulae(
            salesman=salesman,
            commissions_formulae={0: {0: '{p_m}*{m_bc}/{m_mb}*0.06'}})

        self.biz.prestation.salesman.add(
            prestation=presta,
            salesman=salesman)
        self.biz.prestation.salesman.add(
            prestation=another_presta,
            salesman=salesman)
        self.biz.prestation.salesman.add(
            prestation=another_month_presta,
            salesman=salesman)

        self.biz.prestation.cost.create(
            prestation=presta,
            amount=float(100),
            reason=u'Auto Cost 1 P1')
        self.biz.prestation.cost.create(
            prestation=presta,
            amount=float(200),
            reason=u'Auto Cost 2 P1')
        self.biz.prestation.cost.create(
            prestation=another_presta,
            amount=float(100),
            reason=u'Auto Cost 1 P2')
        self.biz.prestation.cost.create(
            prestation=another_month_presta,
            amount=float(100),
            reason=u'Auto Cost 1 P3')

        commission_ideal_p = float(24700)*float(47600)/float(49600)*float(0.06)
        commission_ideal_ap = float(24900)*float(47600)/float(49600)*float(0.06)

        self.assertEqual(presta.prestation_salesmen[0].commission, commission_ideal_p)
        self.assertEqual(another_presta.prestation_salesmen[0].commission, commission_ideal_ap)
        self.assertEqual(month.month_salesmen[0].commission_prestations, commission_ideal_p+commission_ideal_ap)
        self.assertEqual(month.month_salesmen[0].commission_bonuses, float(476))

    def test_get_complexe_commission_two_salesmen(self):
        month_date = datetime.date(year=2012, month=1, day=1)
        another_month_date = datetime.date(year=2012, month=2, day=1)

        self.biz.month.cost.create(
            month_date=month_date,
            amount=float(2000),
            reason=u'NoReason')
        self.biz.month.cost.create(
            month_date=another_month_date,
            amount=float(2000),
            reason=u'NoReason')

        presta = Prestation(
            date=month_date,
            category=0,
            sector=0)
        self.dbsession.add(presta)
        another_presta = Prestation(
            date=month_date,
            category=0,
            sector=0)
        self.dbsession.add(another_presta)
        another_month_presta = Prestation(
            date=another_month_date,
            category=0,
            sector=0)
        self.dbsession.add(another_month_presta)
        self.dbsession.commit()

        self.biz.prestation.bill.create(prestation=presta, ref=u'Bla', amount=float(25000))
        self.biz.prestation.bill.create(prestation=another_presta, ref=u'Bla', amount=float(25000))
        self.biz.prestation.bill.create(prestation=another_month_presta, ref=u'Bla', amount=float(25000))

        salesman = self.biz.salesman.create(
            firstname=u'Bas',
            lastname=u'Gan')
        salesman = self.biz.salesman.set_commissions_formulae(
            salesman=salesman,
            commissions_formulae={0: {0: '{p_m}*{m_bc}/{m_mb}*0.06'}})
        a_salesman = self.biz.salesman.create(
            firstname=u'Bas',
            lastname=u'Gan')
        a_salesman = self.biz.salesman.set_commissions_formulae(
            salesman=a_salesman,
            commissions_formulae={0: {0: '{p_m}*{m_bc}/{m_mb}*0.06'}})

        self.biz.prestation.salesman.add(
            prestation=presta,
            salesman=salesman)
        self.biz.prestation.salesman.add(
            prestation=presta,
            salesman=a_salesman)
        self.biz.prestation.salesman.add(
            prestation=another_presta,
            salesman=salesman)
        self.biz.prestation.salesman.add(
            prestation=another_month_presta,
            salesman=salesman)

        self.biz.prestation.cost.create(
            prestation=presta,
            amount=float(100),
            reason=u'Auto Cost 1 P1')
        self.biz.prestation.cost.create(
            prestation=presta,
            amount=float(200),
            reason=u'Auto Cost 2 P1')
        self.biz.prestation.cost.create(
            prestation=another_presta,
            amount=float(100),
            reason=u'Auto Cost 1 P2')
        self.biz.prestation.cost.create(
            prestation=another_month_presta,
            amount=float(100),
            reason=u'Auto Cost 1 P3')

        commission_ideal_p = float(24700)*float(47600)/float(49600)*float(0.06)*0.5
        commission_ideal_ap = float(24900)*float(47600)/float(49600)*float(0.06)

        self.assertEqual(presta.prestation_salesmen[0].commission, commission_ideal_p)
        self.assertEqual(another_presta.prestation_salesmen[0].commission, commission_ideal_ap)

        month = self.biz.month.get(date=month_date)

        self.assertEqual(month.month_salesmen[0].commission_prestations, commission_ideal_p+commission_ideal_ap)
        self.assertEqual(month.month_salesmen[0].commission_bonuses, float(476))
        self.assertEqual(month.month_salesmen[0].commission_total, float(476)+commission_ideal_p+commission_ideal_ap)
