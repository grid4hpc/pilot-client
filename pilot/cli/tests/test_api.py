from ...cli import api
from ...cli import proxylib
from ...cli import http
import datetime
import pytz
import os
from unittest import TestCase

from mock import Mock

TEST_PILOT = os.environ.get("PILOT_SERVER", 'https://abbot.homeunix.net:5053/jobs/')

class TestOptions:
    capath="/etc/grid-security/certificates"
    use_proxy=True
    proxy=proxylib.get_proxy_filename()
    
def test_JSONEncoder():
    assert api.json_dumps('hello') == '"hello"'
    tz = pytz.tzfile.build_tzinfo("local", open("/etc/localtime"))
    assert api.json_dumps(dict(foo='bar', qux=tz.localize(datetime.datetime(2009, 1, 9, 14, 15, 16)))) == '{"qux": "2009-01-09T14:15:16.000000Z", "foo": "bar"}'
    assert api.json_dumps(dict(foo='bar', qux=datetime.datetime(2009, 1, 9, 14, 15, 16, tzinfo=pytz.utc))) == '{"qux": "2009-01-09T14:15:16.000000Z", "foo": "bar"}'
    assert api.json_dumps(dict(foo='bar', qux=tz.localize(datetime.datetime(2009, 1, 9, 14, 15, 16, 123)))) == '{"qux": "2009-01-09T14:15:16.000123Z", "foo": "bar"}'
    assert api.json_dumps(dict(foo='bar', qux=datetime.datetime(2009, 1, 9, 14, 15, 16, 123, tzinfo=pytz.utc))) == '{"qux": "2009-01-09T14:15:16.000123Z", "foo": "bar"}'
    assert api.json_dumps(dict(x=[dict(foo="bar")])) == '{"x": [{"foo": "bar"}]}'

def test_JSONDecoder():
    data = '{"ts": "2009-01-09T14:15:16Z"}'
    rc = api.json_loads(data)
    assert isinstance(rc['ts'], datetime.datetime)
    assert rc['ts'] == datetime.datetime(2009, 1, 9, 14, 15, 16, tzinfo=pytz.utc)

    data2 = '[ {"ts": "2009-01-09T14:15:16Z", "foo": "bar" }, {"ts": "2009-01-09T14:15:16Z"} ]'
    rc = api.json_loads(data)
    #assert len(rc) == 2
    #assert rc[0]['ts'] == datetime.datetime(2009, 1, 9, 14, 15, 16, tzinfo=pytz.utc)
    #assert rc[0]['foo'] == 'bar'


def test_PilotService_constructor():
    srv = api.PilotService(TEST_PILOT, api.build_ssl_ctx(TestOptions()))
    assert srv.baseurl == TEST_PILOT

class test_handle_http_errors(TestCase):
    def test_errors(self):
        for code in range(400, 409):
            self.assertRaises(SystemExit, api.handle_http_errors, http.Response(code, {}, "", "http://example.com"))
        for code in range(500, 515):
            self.assertRaises(SystemExit, api.handle_http_errors, http.Response(code, {}, "", "http://example.com"))
