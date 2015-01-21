# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest


from magma import souputils as sp


class FakeElement(object):

    def __init__(self, text):
        self.text = text


class TestBase(unittest.TestCase):

    # .text

    def test_text_none(self):
        self.assertEquals(u"", sp.text(None))

    def test_text_strip(self):
        self.assertEquals(u"hello", sp.text(FakeElement(u" hello ")))

    def test_text_strip_newline(self):
        self.assertEquals(u"hello", sp.text(FakeElement(u" hello\n")))

    def test_text_nostrip(self):
        self.assertEquals(u" hello ", sp.text(FakeElement(u" hello "), False))

    # .coursecode

    def test_coursecode_none(self):
        self.assertEquals(u"", sp.coursecode(None))

    def test_coursecode_strip(self):
        self.assertEquals(u"tata", sp.coursecode(FakeElement(u" tata")))

    def test_coursecode_strip_square_brackets(self):
        self.assertEquals(u"abc", sp.coursecode(FakeElement(u"abc [123]")))

    # .parse

    def test_parse_str_none(self):
        self.assertEquals(u"", sp.parse(None, str))

    def test_parse_int_none(self):
        self.assertEquals(0, sp.parse(None, int))

    def test_parse_float_none(self):
        self.assertEquals(0.0, sp.parse(None, float))

    def test_parse_bool_none(self):
        self.assertFalse(sp.parse(None, bool))

    def test_parse_str_empty_text(self):
        self.assertEquals(u"", sp.parse(FakeElement(u""), str))

    def test_parse_int_empty_text(self):
        self.assertEquals(0, sp.parse(FakeElement(u""), int))

    def test_parse_float_empty_text(self):
        self.assertEquals(0.0, sp.parse(FakeElement(u""), float))

    def test_parse_bool_empty_text(self):
        self.assertFalse(sp.parse(FakeElement(u""), bool))

    def test_parse_bool_spaces_only(self):
        self.assertFalse(sp.parse(FakeElement(u"   \n"), bool))

    def test_parse_int(self):
        self.assertEquals(42, sp.parse(FakeElement(u" 42"), int))

    # .parseint

    def test_parseint(self):
        self.assertEquals(42, sp.parseint(FakeElement(u"42\n")))

    # .parsefloat

    def test_parsefloat(self):
        self.assertEquals(3.14, sp.parsefloat(FakeElement(u" 3.14")))

    # .parsebool

    def test_parsebool_oui(self):
        self.assertTrue(sp.parsebool(FakeElement(u"oui ")))
        self.assertTrue(sp.parsebool(FakeElement(u"\nOUI ")))

    def test_parsebool_non(self):
        self.assertFalse(sp.parsebool(FakeElement(u"non ")))
        self.assertFalse(sp.parsebool(FakeElement(u" NON")))

    def test_parsebool_int_true(self):
        self.assertTrue(sp.parsebool(FakeElement(u"42")))

    def test_parsebool_int_false(self):
        self.assertFalse(sp.parsebool(FakeElement(u"0")))
