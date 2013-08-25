# -*- encoding: utf-8 -*-

from unittest import TestCase
from .. import http

BASE = "https://abbot.homeunix.net:5053"

class TestHttp(TestCase):
    def setUp(self):
        self.http = http.HTTP(BASE + "/some/path")

    def test_actual_uri(self):
        self.assertEqual(self.http._actual_uri("http://example.com"), "http://example.com")
        self.assertEqual(self.http._actual_uri("/hello"), BASE + "/hello")

    def test_unsupported_protocol(self):
        self.assertRaises(http.Error, self.http.request, "GET", "ftp://example.com")

    def test_headers(self):
        h = self.http._prepare_headers({}, None)
        self.assertEqual(h["content-length"], "0")
        self.assertEqual(h["connection"], "close")
        self.assertTrue("user-agent" in h)
        self.assertFalse("content-type" in h)

        data = u"test"
        h = self.http._prepare_headers({}, data)
        self.assertEqual(h["content-length"], "4")
        self.assertEqual(h["content-md5"], "CY9rzUYh03PK3k6DJie09g==")
        self.assertTrue("content-type" in h)
        self.assertEqual(h["content-type"], "application/json")

        h = self.http._prepare_headers({"Content-Type": "text/plain", "content-length": "100"}, data)
        self.assertEqual(h["content-length"], "4")
        self.assertEqual(h["content-md5"], "CY9rzUYh03PK3k6DJie09g==")
        self.assertTrue("content-type" in h)
        self.assertEqual(h["content-type"], "text/plain")
