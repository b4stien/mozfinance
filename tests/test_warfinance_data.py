 # -*- coding: utf-8 -*-
import unittest

from mozfinance.data import ModelPackageChecker as PackageChecker
from mozfinance.data import DataRepository

from . import TestData


class TestModelBase(unittest.TestCase):

    def test_action(self):
        package_checker = PackageChecker(package='mozfinance.data.model')
        self.assertTrue(package_checker.run())


class TestWarfdataInit(TestData):

    def test_correct_datarepo_init(self):
        DataRepository(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user
        )

    def test_no_datarepo(self):
        with self.assertRaises(TypeError):
            DataRepository(
                dbsession=self.dbsession,
                user=self.user)

    def test_no_session(self):
        with self.assertRaises(TypeError):
            DataRepository(
                package='mozfinance.data.model',
                user=self.user
            )

    def test_wrong_session(self):
        with self.assertRaises(AttributeError):
            DataRepository(
                package='mozfinance.data.model',
                dbsession='not session',
                user=self.user
            )

    def test_datarepo_init_user_id(self):
        DataRepository(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user_id=self.user.id
        )

    def test_no_user(self):
        with self.assertRaises(TypeError):
            DataRepository(
                package='mozfinance.data.model',
                dbsession=self.dbsession
            )

    def test_wrong_user(self):
        with self.assertRaises(AttributeError):
            DataRepository(
                package='mozfinance.data.model',
                dbsession=self.dbsession,
                user='not a SQLA-user'
            )


if __name__ == '__main__':
    unittest.main()
