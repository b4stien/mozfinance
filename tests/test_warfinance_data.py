 # -*- coding: utf-8 -*-
import unittest

from warfinance.data import ModelPackageChecker as PackageChecker
from warfinance.data import DataRepository

from . import TestData


class TestModelBase(unittest.TestCase):

    def test_action(self):
        package_checker = PackageChecker(package='warfinance.data.model')
        self.assertTrue(package_checker.run())


class TestWarfdataInit(TestData):

    def test_correct_datarepo_init(self):
        datarepo = DataRepository(
            package='warfinance.data.model',
            session=self.session,
            user=self.user
        )

    def test_no_datarepo(self):
        with self.assertRaises(TypeError):
            datarepo = DataRepository(
                session=self.session,
                user=self.user)

    def test_no_session(self):
        with self.assertRaises(TypeError):
            datarepo = DataRepository(
                package='warfinance.data.model',
                user=self.user
            )

    def test_wrong_session(self):
        with self.assertRaises(AttributeError):
            datarepo = DataRepository(
                package='warfinance.data.model',
                session='not session',
                user=self.user
            )

    def test_datarepo_init_user_id(self):
        datarepo = DataRepository(
            package='warfinance.data.model',
            session=self.session,
            user_id=self.user.id
        )

    def test_no_user(self):
        with self.assertRaises(TypeError):
            datarepo = DataRepository(
                package='warfinance.data.model',
                session=self.session
            )

    def test_wrong_user(self):
        with self.assertRaises(AttributeError):
            datarepo = DataRepository(
                package='warfinance.data.model',
                session=self.session,
                user='not a SQLA-user'
            )


if __name__ == '__main__':
    unittest.main()
