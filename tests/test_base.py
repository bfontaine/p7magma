# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

from magma import base


class TestBase(unittest.TestCase):

    pass  # TODO
