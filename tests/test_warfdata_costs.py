 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

import warbmodel
from warbmodel import *
from warbdata.users import UsersData
from warbdata.applications import ApplicationsData

from warfdata.model import *
from warfdata.costs import CostsData


class TestCreateCost(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        warbmodel.Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
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

        self.costs_data = CostsData(
            application=self.app,
            package='warfdata.model',
            session=self.session,
            user=self.user)
        self.prestation = Prestation.Prestation()

    def tearDown(self):
        del self.session
        del self.users_data

    def test_correct_minimal_create(self):
        cost = self.costs_data.create(
            reason=u'Achat de traôneau',
            prestation=self.prestation,
            pop_action=False)
        self.assertTrue(isinstance(cost, Cost.Cost))
        self.assertEqual(u'Achat de traôneau', cost.reason)
        self.assertEqual(cost.prestation, self.prestation)
        with self.assertRaises(NoResultFound):
            self.session.query(Action.Action).one()

    def test_correct_create_with_action(self):
        cost = self.costs_data.create(
            reason=u'With action',
            prestation=self.prestation,
            pop_action=True)
        action = self.session.query(Action.Action).one()
        print action.message.encode('utf-8')


if __name__ == '__main__':
    unittest.main()
