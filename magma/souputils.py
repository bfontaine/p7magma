# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import re


def text(el, strip=True):
    """
    Return the text of a ``BeautifulSoup`` element
    """
    if not el:
        return ""

    text = el.text
    if strip:
        text = text.strip()
    return text  # .encode("utf-8")


def coursecode(el):
    """
    Return the text of a ``BeautifulSoup`` element, assuming it's a course code
    (it strips any square-brackets-surrounded number at its end).
    """
    txt = text(el)
    return re.sub(r"\s*\[\d+\]$", "", txt, re.UNICODE)


def parse(el, typ):
    """
    Parse a ``BeautifulSoup`` element as the given type.
    """
    if not el:
        return typ()
    txt = text(el)
    if not txt:
        return typ()
    return typ(txt)


def parseint(el):
    """
    Parse a ``BeautifulSoup`` element as an int
    """
    return parse(el, int)


def parsefloat(el):
    """
    Parse a ``BeautifulSoup`` element as float
    """
    return parse(el, float)


def parseresult(el):
    s = text(el)
    if s == "ABI":
        return s
    return parsefloat(el)


def parsebool(el):
    """
    Parse a ``BeautifulSoup`` element as a bool
    """
    txt = text(el)
    up = txt.upper()
    if up == "OUI":
        return True
    if up == "NON":
        return False

    return bool(parseint(el))
