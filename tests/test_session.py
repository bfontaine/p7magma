# -*- coding: UTF-8 -*-
# Most of these tests are based on didelcli's:
#   https://github.com/bfontaine/didelcli/blob/master/tests/test_session.py

from __future__ import unicode_literals

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

import requests
import responses

from magma.session import Session

class TestSession(unittest.TestCase):

    def test_ua_set_on_init(self):
        ua = 'th+is/an user 4gent'
        s = Session(user_agent=ua)
        self.assertEquals(ua, s.user_agent)

    def test_set_headers_defaults_user_agent_already_present(self):
        ua = 'some/random - user+agent v42.1.3.21'
        kwargs = {'headers': {'User-Agent': ua}}
        s = Session(user_agent='another/user_agent v1')
        s._set_header_defaults(kwargs)  # in-place change
        self.assertEquals(ua, kwargs['headers']['User-Agent'])

    def test_set_headers_defaults_user_agent_not_present_no_headers(self):
        ua = 'some/random - user+agent v42.1.3.21'
        kwargs = {}
        s = Session(user_agent=ua)
        s._set_header_defaults(kwargs)  # in-place change
        self.assertIn('headers', kwargs)
        self.assertEquals(ua, kwargs['headers']['User-Agent'])

    def test_set_headers_defaults_user_agent_not_present_with_headers(self):
        ua = 'some/random - user+agent v42.1.3.21'
        kwargs = {'headers': {'X-Foo': '42'}}
        s = Session(user_agent=ua)
        s._set_header_defaults(kwargs)  # in-place change
        self.assertIn('headers', kwargs)
        self.assertEquals(ua, kwargs['headers']['User-Agent'])


    # .get_url

    def test_get_absolute_url(self):
        url = 'http://example.com'
        s = Session()
        self.assertEquals(url, s.get_url(url))

    def test_get_relative_url_root_with_base_url(self):
        url = '/'
        s = Session(base_url="foobar")
        self.assertEquals("http://foobar/", s.get_url(url))

    def test_get_relative_url_with_base_url(self):
        s = Session(base_url="abc")
        self.assertEquals('http://abc/foo/bar/qux', s.get_url("/foo/bar/qux"))


    # .get

    @responses.activate
    def test_get_requests_object(self):
        url = 'http://www.example.com/foo'
        body = "okx&Asq'"
        responses.add(responses.GET, url, body=body, status=200)
        s = Session()
        resp = s.get(url)
        self.assertEquals(1, len(responses.calls))
        self.assertIsInstance(resp, requests.Response)

    @responses.activate
    def test_get_set_default_ua(self):
        url = 'http://www.example.com/foo'
        responses.add(responses.GET, url, body='ok', status=200)
        Session().get(url)
        self.assertEquals(1, len(responses.calls))
        self.assertIn('User-Agent', responses.calls[0].request.headers)

    @responses.activate
    def test_post_requests_object(self):
        url = 'http://www.example.com/foo'
        body = "okx&Asq'"
        responses.add(responses.POST, url, body=body, status=200)
        s = Session()
        resp = s.post(url)
        self.assertEquals(1, len(responses.calls))
        self.assertIsInstance(resp, requests.Response)
