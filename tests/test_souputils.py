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
        self.assertEquals("", sp.text(None))

    def test_text_strip(self):
        self.assertEquals("hello", sp.text(FakeElement(" hello ")))

    def test_text_strip_newline(self):
        self.assertEquals("hello", sp.text(FakeElement(" hello\n")))

    def test_text_nostrip(self):
        self.assertEquals(" hello ", sp.text(FakeElement(" hello "), False))

    # .coursecode

    def test_coursecode_none(self):
        self.assertEquals("", sp.coursecode(None))

    def test_coursecode_strip(self):
        self.assertEquals("tata", sp.coursecode(FakeElement(" tata")))

    def test_coursecode_strip_square_brackets(self):
        self.assertEquals("abc", sp.coursecode(FakeElement("abc [123]")))

    # .parse

    def test_parse_str_none(self):
        self.assertEquals("", sp.parse(None, str))

    def test_parse_int_none(self):
        self.assertEquals(0, sp.parse(None, int))

    def test_parse_float_none(self):
        self.assertEquals(0.0, sp.parse(None, float))

    def test_parse_bool_none(self):
        self.assertFalse(sp.parse(None, bool))

    def test_parse_str_empty_text(self):
        self.assertEquals("", sp.parse(FakeElement(""), str))

    def test_parse_int_empty_text(self):
        self.assertEquals(0, sp.parse(FakeElement(""), int))

    def test_parse_float_empty_text(self):
        self.assertEquals(0.0, sp.parse(FakeElement(""), float))

    def test_parse_bool_empty_text(self):
        self.assertFalse(sp.parse(FakeElement(""), bool))

    def test_parse_bool_spaces_only(self):
        self.assertFalse(sp.parse(FakeElement("   \n"), bool))

    def test_parse_int(self):
        self.assertEquals(42, sp.parse(FakeElement(" 42"), int))

    # .parseint

    def test_parseint(self):
        self.assertEquals(42, sp.parseint(FakeElement("42\n")))

    # .parsefloat

    def test_parsefloat(self):
        self.assertEquals(3.14, sp.parsefloat(FakeElement(" 3.14")))

    # .parsebool

    def test_parsebool_oui(self):
        self.assertTrue(sp.parsebool(FakeElement("oui ")))
        self.assertTrue(sp.parsebool(FakeElement("\nOUI ")))

    def test_parsebool_non(self):
        self.assertFalse(sp.parsebool(FakeElement("non ")))
        self.assertFalse(sp.parsebool(FakeElement(" NON")))

    def test_parsebool_int_true(self):
        self.assertTrue(sp.parsebool(FakeElement("42")))

    def test_parsebool_int_false(self):
        self.assertFalse(sp.parsebool(FakeElement("0")))
