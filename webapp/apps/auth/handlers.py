from tornado import gen
from modules.http import handlers


class SocialAuthUrlHandler(handlers.BaseHandler):
    def do_get(self, *args, **kwargs):
        return {'hello': 'world'}

    def do_post(self, *args, **kwargs):
        return {'hello': 'world'}


class AsyncSocialAuthUrlHandler(handlers.AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        raise gen.Return({'hello': 'world'})

    @gen.coroutine
    def do_post(self, *args, **kwargs):
        raise gen.Return({'hello': 'world'})
