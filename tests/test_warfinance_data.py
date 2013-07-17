 # -*- coding: utf-8 -*-
import unittest

from mozfinance.data import DataRepository

from . import TestData


class TestWarfdataInit(TestData):

    def test_correct_datarepo_init(self):
        class Bli():
            _dbsession = self.dbsession
            _package = 'lol'

        DataRepository(bo=Bli())

    def test_no_datarepo(self):
        with self.assertRaises(TypeError):
            DataRepository(dbsession=self.dbsession)

    def test_no_session(self):
        with self.assertRaises(TypeError):
            DataRepository(package='mozfinance.data.model')

    def test_session_wo_cache(self):
        with self.assertRaises(TypeError):
            DataRepository(
                package='mozfinance.data.model',
                dbsession='not session')


if __name__ == '__main__':
    unittest.main()
