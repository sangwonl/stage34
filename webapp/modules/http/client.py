from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httputil import HTTPHeaders

import json


@gen.coroutine
def fetch(url, method, headers=None, body=None):
    headers.update({'User-Agent': 'Tornado/4.4.1'})
    req = HTTPRequest(url=url, method=method, headers=headers, body=body)
    http_client = AsyncHTTPClient()
    res = yield http_client.fetch(req)
    raise gen.Return(res)