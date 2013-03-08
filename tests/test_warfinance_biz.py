 # -*- coding: utf-8 -*-
import unittest

from warfinance.biz import BusinessWorker

from . import TestData


class TestBiz(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.biz = BusinessWorker(
            package='warfinance.data.model',
            session=self.session,
            user=self.user)

    def test_base(self):
        pass


    def tearDown(self):
        TestData.tearDown(self)
        del self.biz
    