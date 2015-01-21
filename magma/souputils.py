# -*- coding: UTF-8 -*-

import re

def text(el, strip=True):
    if not el:
        return ""

    text = el.text
    if strip:
        text = text.strip()
    return text.encode("utf-8")


def coursecode(el):
    txt = text(el)
    return re.sub(r"\s*\[\d+\]$", u"", txt)


def parse(el, typ):
    if not el:
        return typ()
    txt = text(el)
    if not txt:
        return typ()
    return typ(txt)


def parseint(el):
    return parse(el, int)

def parsefloat(el):
    return parse(el, float)

def parsebool(el):
    txt = text(el)
    up = txt.upper()
    if up == u"OUI":
        return True
    if up == u"NON":
        return False

    return bool(parseint(el))
