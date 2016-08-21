from tornado import gen

from modules.http.handlers import AsyncBaseHandler
from modules.http import JSENDSuccess, JSENDError

from conf import settings


class StageRootHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        res = JSENDSuccess(status_code=200, data={})
        raise gen.Return(res)


class StageDetailHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        res = JSENDSuccess(status_code=200, data={})
        raise gen.Return(res)