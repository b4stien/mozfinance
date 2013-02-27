 # -*- coding: utf-8 -*-
import unittest

from warfinance.biz import BusinessWorker

from . import TestData


class TestBusiness(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.biz = BusinessWorker(
            application=self.app,
            package='warfinance.data.model',
            session=self.session,
            user=self.user)


    def tearDown(self):
        TestData.tearDown(self)
        del self.biz


class TestBusinessBase(TestBusiness):

    def test_base(self):
        pass