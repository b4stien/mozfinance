 # -*- coding: utf-8 -*-
import unittest

from warfdata import ModelPackageChecker as PackageChecker


class TestModelBase(unittest.TestCase):

    def test_action(self):
        package_checker = PackageChecker(package='warfdata.model')
        self.assertTrue(package_checker.run())


if __name__ == '__main__':
    unittest.main()
