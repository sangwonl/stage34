from tornado import gen
from conf import settings

from modules.http.handlers import BaseHandler, AsyncBaseHandler
from modules.http import JSENDSuccess

import uuid
import urllib


class GithubAuthUrlHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        github_conf = settings.get('github')
        query_params = {
            'redirect_uri': github_conf.get('redirect_uri'),
            'client_id': github_conf.get('client_id'),
            'scope': github_conf.get('scope'),
            'state': str(uuid.uuid4().hex),
            'response_type': 'code'
        }

        res = JSENDSuccess(status_code=200, data={
            'authorize_url': '%s?%s' % (
                github_conf.get('auth_url'),
                urllib.urlencode(query_params))
        })
        raise gen.Return(res)


class GithubCallbackHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        code = self.get_argument('code', None)
        state = self.get_argument('state', None)
        res = JSENDSuccess(status_code=200, data={
            'code': code,
            'state': state
        })
        raise gen.Return(res)