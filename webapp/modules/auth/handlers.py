from tornado import gen

from modules.base import AsyncBaseHandler
from modules.base import BaseHandler


class SocialAuthUrlHandler(BaseHandler):
    def do_get(self, *args, **kwargs):
        return {'hello': 'world'}

    def do_post(self, *args, **kwargs):
        return {'hello': 'world'}


class AsyncSocialAuthUrlHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        raise gen.Return({'hello': 'world'})

    @gen.coroutine
    def do_post(self, *args, **kwargs):
        raise gen.Return({'hello': 'world'})
