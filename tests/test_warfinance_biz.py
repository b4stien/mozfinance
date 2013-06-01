 # -*- coding: utf-8 -*-
import unittest

from mozfinance.biz import BusinessWorker

from . import TestData


class TestBiz(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.biz = BusinessWorker(
            package='mozfinance.data.model',
            dbsession=self.dbsession,
            user=self.user)

    def test_base(self):
        pass


    def tearDown(self):
        TestData.tearDown(self)
        del self.biz
