from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

import json


@gen.coroutine
def fetch(url, method, headers=None, body=None):
    req = HTTPRequest(url=url, method=method, headers=headers, body=body)
    http_client = AsyncHTTPClient()
    res = yield http_client.fetch(req)
    raise gen.Return(res)