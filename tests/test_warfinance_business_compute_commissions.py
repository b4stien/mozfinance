 # -*- coding: utf-8 -*-
import datetime

from warfinance.data.model.Prestation import Prestation
from warfinance.biz import BusinessWorker
import warfinance

from . import TestData


class TestBusinessCompute(TestData):

    def setUp(self):
        TestData.setUp(self)

        def a_bonus(**kwargs):
            if kwargs['m_mn'] >= float(10000):
                return 0.01*kwargs['m_mn']

            return float(0)

        if not a_bonus in warfinance.COMMISSIONS_BONUS:
            warfinance.COMMISSIONS_BONUS.append(a_bonus)

        self.biz = BusinessWorker(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def tearDown(self):
        TestData.tearDown(self)
        warfinance.COMMISSIONS_BONUS = []
        del self.biz

    def test_get_simple_commission(self):
        now = datetime.datetime.now()
        now_date = now.date()
        month_date = datetime.date(year=now.year, month=now.month, day=1)

        self.biz.data.months.create(
            date=month_date,
            cost=float(2000))

        presta = Prestation(
            date=now_date,
            selling_price=float(4000),
            category=0,
            sector=0)
        self.session.add(presta)
        self.session.commit()

        salesman = self.biz.data.salesmen.create(
            firstname=u'Bas',
            lastname=u'Gan')
        salesman = self.biz.data.salesmen.set_commissions_formulae(
            salesman=salesman,
            commissions_formulae={0: {0: '{p_m}*{m_mn}/{m_mb}*0.06'}})

        self.biz.data.prestations.add_salesman(
            prestation=presta,
            salesman=salesman)

        self.biz.data.costs.create(
            prestation=presta,
            amount=float(100),
            reason=u'Auto Cost 1')

        salesmen_dict = self.biz._compute.prestation_salesmen(
            prestation=presta,
            compute=True)

        month_salesman_dict = self.biz._compute.month_salesmen(
            date=month_date,
            compute=True)

        commission_ideal = float(3900)*float(1900)/float(3900)*float(0.06)

        self.assertEqual(salesmen_dict[salesman.id]['formula'], '{p_m}*{m_mn}/{m_mb}*0.06')
        self.assertEqual(salesmen_dict[salesman.id]['commission'], commission_ideal)
        self.assertEqual(month_salesman_dict[salesman.id]['total_prestations'], commission_ideal)

    def test_get_complexe_commission(self):
        month_date = datetime.date(year=2013, month=1, day=1)
        another_month_date = datetime.date(year=2013, month=2, day=1)

        self.biz.data.months.create(
            date=month_date,
            cost=float(2000))
        self.biz.data.months.create(
            date=another_month_date,
            cost=float(2000))

        presta = Prestation(
            date=month_date,
            selling_price=float(25000),
            category=0,
            sector=0)
        self.session.add(presta)
        another_presta = Prestation(
            date=month_date,
            selling_price=float(25000),
            category=0,
            sector=0)
        self.session.add(another_presta)
        another_month_presta = Prestation(
            date=another_month_date,
            selling_price=float(25000),
            category=0,
            sector=0)
        self.session.add(another_month_presta)
        self.session.commit()

        salesman = self.biz.data.salesmen.create(
            firstname=u'Bas',
            lastname=u'Gan')
        salesman = self.biz.data.salesmen.set_commissions_formulae(
            salesman=salesman,
            commissions_formulae={0: {0: '{p_m}*{m_mn}/{m_mb}*0.06'}})

        self.biz.data.prestations.add_salesman(
            prestation=presta,
            salesman=salesman)
        self.biz.data.prestations.add_salesman(
            prestation=another_presta,
            salesman=salesman)
        self.biz.data.prestations.add_salesman(
            prestation=another_month_presta,
            salesman=salesman)

        self.biz.data.costs.create(
            prestation=presta,
            amount=float(100),
            reason=u'Auto Cost 1 P1')
        self.biz.data.costs.create(
            prestation=presta,
            amount=float(200),
            reason=u'Auto Cost 2 P1')
        self.biz.data.costs.create(
            prestation=another_presta,
            amount=float(100),
            reason=u'Auto Cost 1 P2')
        self.biz.data.costs.create(
            prestation=another_month_presta,
            amount=float(100),
            reason=u'Auto Cost 1 P3')

        p_salesmen_dict = self.biz._compute.prestation_salesmen(
            prestation=presta,
            compute=True)
        ap_salesmen_dict = self.biz._compute.prestation_salesmen(
            prestation=another_presta,
            compute=True)

        month_salesman_dict = self.biz._compute.month_salesmen(
            date=month_date,
            compute=True)

        commission_ideal_p = float(24700)*float(47600)/float(49600)*float(0.06)
        commission_ideal_ap = float(24900)*float(47600)/float(49600)*float(0.06)

        self.assertEqual(p_salesmen_dict[salesman.id]['commission'], commission_ideal_p)
        self.assertEqual(ap_salesmen_dict[salesman.id]['commission'], commission_ideal_ap)
        self.assertEqual(month_salesman_dict[salesman.id]['total_prestations'], commission_ideal_p+commission_ideal_ap)
        self.assertEqual(month_salesman_dict[salesman.id]['total_bonuses'], float(476))

    def test_get_complexe_commission_two_salesmen(self):
        now = datetime.datetime.now()
        now_date = now.date()
        month_date = datetime.date(year=now.year, month=now.month, day=1)
        another_month_date = datetime.date(year=now.year-1, month=now.month, day=1)

        self.biz.data.months.create(
            date=month_date,
            cost=float(2000))
        self.biz.data.months.create(
            date=another_month_date,
            cost=float(2000))

        presta = Prestation(
            date=now_date,
            selling_price=float(25000),
            category=0,
            sector=0)
        self.session.add(presta)
        another_presta = Prestation(
            date=now_date,
            selling_price=float(25000),
            category=0,
            sector=0)
        self.session.add(another_presta)
        another_month_presta = Prestation(
            date=another_month_date,
            selling_price=float(25000),
            category=0,
            sector=0)
        self.session.add(another_month_presta)
        self.session.commit()

        salesman = self.biz.data.salesmen.create(
            firstname=u'Bas',
            lastname=u'Gan')
        salesman = self.biz.data.salesmen.set_commissions_formulae(
            salesman=salesman,
            commissions_formulae={0: {0: '{p_m}*{m_mn}/{m_mb}*0.06'}})
        a_salesman = self.biz.data.salesmen.create(
            firstname=u'Bas',
            lastname=u'Gan')
        a_salesman = self.biz.data.salesmen.set_commissions_formulae(
            salesman=a_salesman,
            commissions_formulae={0: {0: '{p_m}*{m_mn}/{m_mb}*0.06'}})

        self.biz.data.prestations.add_salesman(
            prestation=presta,
            salesman=salesman)
        self.biz.data.prestations.add_salesman(
            prestation=presta,
            salesman=a_salesman)
        self.biz.data.prestations.add_salesman(
            prestation=another_presta,
            salesman=salesman)
        self.biz.data.prestations.add_salesman(
            prestation=another_month_presta,
            salesman=salesman)

        self.biz.data.costs.create(
            prestation=presta,
            amount=float(100),
            reason=u'Auto Cost 1 P1')
        self.biz.data.costs.create(
            prestation=presta,
            amount=float(200),
            reason=u'Auto Cost 2 P1')
        self.biz.data.costs.create(
            prestation=another_presta,
            amount=float(100),
            reason=u'Auto Cost 1 P2')
        self.biz.data.costs.create(
            prestation=another_month_presta,
            amount=float(100),
            reason=u'Auto Cost 1 P3')

        p_salesmen_dict = self.biz._compute.prestation_salesmen(
            prestation=presta,
            compute=True)
        ap_salesmen_dict = self.biz._compute.prestation_salesmen(
            prestation=another_presta,
            compute=True)

        month_salesman_dict = self.biz._compute.month_salesmen(
            date=month_date,
            compute=True)

        commission_ideal_p = float(24700)*float(47600)/float(49600)*float(0.06)*0.5
        commission_ideal_ap = float(24900)*float(47600)/float(49600)*float(0.06)

        self.assertEqual(p_salesmen_dict[salesman.id]['commission'], commission_ideal_p)
        self.assertEqual(ap_salesmen_dict[salesman.id]['commission'], commission_ideal_ap)
        self.assertEqual(month_salesman_dict[salesman.id]['total_prestations'], commission_ideal_p+commission_ideal_ap)
        self.assertEqual(month_salesman_dict[salesman.id]['total_bonuses'], float(476))
        self.assertEqual(month_salesman_dict[salesman.id]['commission'], float(476)+commission_ideal_p+commission_ideal_ap)
