# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

import magma


class TestVersion(unittest.TestCase):

    def test_version(self):
        self.assertRegexpMatches(magma.__version__, r'^\d+\.\d+\.\d+')
