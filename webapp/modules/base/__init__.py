from tornado import gen
from tornado import web
from tornado import websocket
from tornado.web import HTTPError


class WSBaseHandler(websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(WSBaseHandler, self).__init__(application, request, **kwargs)

    def on_message(self, message):
        raise NotImplementedError()

    def data_received(self, chunk):
        pass


class BaseHandler(web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def data_received(self, chunk):
        pass

    def do_get(self, *args, **kwargs):
        raise NotImplementedError()

    def do_post(self, *args, **kwargs):
        raise NotImplementedError()

    def handle(self, do_func, *args, **kwargs):
        res = do_func(args, kwargs)
        self.write(res)

    def get(self, *args, **kwargs):
        self.handle(self.do_get, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.handle(self.do_post, *args, **kwargs)


class AsyncBaseHandler(BaseHandler):
    @gen.coroutine
    def handle(self, do_func, *args, **kwargs):
        res = yield do_func(args, kwargs)
        self.write(res)

    @gen.coroutine
    def get(self, *args, **kwargs):
        yield self.handle(self.do_get, *args, **kwargs)

    @gen.coroutine
    def post(self, *args, **kwargs):
        yield self.handle(self.do_post, *args **kwargs)
