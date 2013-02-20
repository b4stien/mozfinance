 # -*- coding: utf-8 -*-
import unittest

from warfdata import ModelPackageChecker as PackageChecker
from warfdata import DataRepository

from . import TestData


class TestModelBase(unittest.TestCase):

    def test_action(self):
        package_checker = PackageChecker(package='warfdata.model')
        self.assertTrue(package_checker.run())


class TestWarfdataInit(TestData):

    def test_correct_datarepo_init(self):
        datarepo = DataRepository(
            application=self.app,
            package='warfdata.model',
            session=self.session,
            user=self.user
        )

    def test_no_session(self):
        with self.assertRaises(TypeError):
            datarepo = DataRepository(
                application=self.app,
                package='warfdata.model',
                user=self.user
            )

    def test_wrong_session(self):
        with self.assertRaises(AttributeError):
            datarepo = DataRepository(
                application=self.app,
                package='warfdata.model',
                session='not session',
                user=self.user
            )

    def test_datarepo_init_user_id(self):
        datarepo = DataRepository(
            application=self.app,
            package='warfdata.model',
            session=self.session,
            user_id=self.user.id
        )

    def test_no_user(self):
        with self.assertRaises(TypeError):
            datarepo = DataRepository(
                application=self.app,
                package='warfdata.model',
                session=self.session
            )

    def test_wrong_user(self):
        with self.assertRaises(AttributeError):
            datarepo = DataRepository(
                application=self.app,
                package='warfdata.model',
                session=self.session,
                user='not a SQLA-user'
            )

    def test_datarepo_init_app_id(self):
        datarepo = DataRepository(
            application_id=self.app.id,
            package='warfdata.model',
            session=self.session,
            user_id=self.user.id
        )

    def test_no_app(self):
        with self.assertRaises(TypeError):
            datarepo = DataRepository(
                package='warfdata.model',
                session=self.session,
                user_id=self.user.id
            )

    def test_wrong_app(self):
        with self.assertRaises(AttributeError):
            datarepo = DataRepository(
                application='self.app',
                package='warfdata.model',
                session=self.session,
                user=self.user
            )


if __name__ == '__main__':
    unittest.main()
