from tornado import gen

from modules.http.handlers import BaseHandler, AsyncBaseHandler
from modules.http import JSENDSuccess
from modules.agents.github import GithubAgent


class GithubAuthUrlHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        auth_url = GithubAgent.get_authorize_url()
        res = JSENDSuccess(status_code=200, data={'authorize_url': auth_url})
        raise gen.Return(res)


class GithubCallbackHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        state = self.get_argument('state', None)
        code = self.get_argument('code', None)
        access_token = yield GithubAgent.request_access_token(state, code)
        self.set_secure_cookie('github-access-token', access_token)
        self.redirect('/')
