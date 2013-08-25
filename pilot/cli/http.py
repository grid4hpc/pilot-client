# -*- encoding: utf-8 -*-

import functools
import socket
import hashlib
from urlparse import urlparse, urlunparse
import httplib
from M2Crypto import httpslib

from collections import namedtuple

class Response(namedtuple("Response", "status headers body url")):
    __slots__ = ()

class Error(RuntimeError):
    pass

class HTTP(object):
    """
    Do HTTP/HTTPS requests for given base service url and with ssl_context
    """

    nonfatal_exceptions = [socket.timeout, httplib.BadStatusLine]

    # FIXME: insert package version into default UA string
    def __init__(self, base_url="", ssl_context=None,
                 ua="pilot-client", timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                 retries=1):
        self.base_url = urlparse(base_url)
        self.ssl_context = ssl_context
        self.ua = ua
        self.timeout = timeout
        self.retries = retries

    def _actual_uri(self, uri):
        parts = list(urlparse(uri))
        # check netloc, replace scheme and netloc for relative paths
        for i in range(0,2):
            if parts[i] == "":
                parts[i] = self.base_url[i]

        return urlunparse(parts)     

    def _prepare_headers(self, headers, body):
        if headers is None:
            headers = {}
        headers = dict((k.lower(), v) for k, v in headers.iteritems())
        headers.setdefault('user-agent', self.ua)
        headers["connection"] = "close"
        
        if body:
            if isinstance(body, unicode):
                body = body.encode("utf-8")
            headers["content-length"] = "{0}".format(len(body))
            headers["content-md5"] = hashlib.md5(body).digest().encode("base64").strip()
            headers.setdefault("content-type", "application/json")
        else:
            headers["content-length"] = "0"

        return headers

    def _make_connection(self, p_uri):
        if ':' in p_uri.netloc:
            host, port = p_uri.netloc.split(':')
            port = int(port)
        else:
            host = p_uri.netloc
            port = socket.getservbyname(p_uri.scheme)

        if p_uri.scheme == "http":
            return httplib.HTTPConnection(host, port)
        else:
            return httpslib.HTTPSConnection(host, port, ssl_context=self.ssl_context)            

    def request(self, method, uri, headers=None, body=None):
        p_uri = urlparse(self._actual_uri(uri))
        if p_uri.scheme not in ("http", "https"):
            raise Error("Unsupported protocol in URI: {0}".format(uri))

        headers = self._prepare_headers(headers, body)

        attempt = 0
        while attempt < self.retries:
            attempt += 1
            try:
                conn = self._make_connection(p_uri)
                conn.request(method, p_uri.path, body, headers)
                response = conn.getresponse()
                data = response.read()
                return Response(response.status, dict(response.getheaders()), data, p_uri.geturl())
            except Exception, exc:
                if type(exc) in self.nonfatal_exceptions:
                    if attempt < self.retries:
                        continue
                    else:
                        raise
                else:
                    raise

    class _verb(object):
        def __init__(self, name):
            self.name = name

        def __get__(self, object, type=None):
            return functools.partial(object.request, self.name)

    get = _verb("GET")
    put = _verb("PUT")
    delete = _verb("DELETE")
    post = _verb("POST")
