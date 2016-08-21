from app import TornadoApplication
from tornado.testing import AsyncHTTPTestCase

import json
import urllib


class HttpTestCase(AsyncHTTPTestCase):
    def __init__(self, methodName='runTest', **kwargs):
        super(HttpTestCase, self).__init__(methodName, **kwargs)

    def get_app(self):
        return TornadoApplication(io_loop=self.io_loop)

    def req(self, url=None, method=None, headers=None, body=None, content_type='json'):
        res = self.fetch(path=url, method=method.upper(), headers=headers, body=body)
        return json.loads(res.body) if content_type == 'json' else res.body
