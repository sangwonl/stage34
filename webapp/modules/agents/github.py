from tornado import gen
from conf import settings

from modules.http import client as httpclient

import uuid
import urllib
import json


class GithubAgent(object):
    def __init__(self):
        pass

    @staticmethod
    def get_authorize_url():
        github_conf = settings.get('github')
        query_params = {
            'redirect_uri': github_conf.get('redirect_uri'),
            'client_id': github_conf.get('client_id'),
            'scope': github_conf.get('scope'),
            'state': str(uuid.uuid4().hex),
            'response_type': 'code'
        }

        github_auth_base_url = github_conf.get('authorize_url')
        urlencoded_query_parms = urllib.urlencode(query_params)
        return '%s?%s' % (github_auth_base_url, urlencoded_query_parms)

    @staticmethod
    @gen.coroutine
    def request_access_token(state, code):
        github_conf = settings.get('github')
        json_params = {
            'client_id': github_conf.get('client_id'),
            'client_secret': github_conf.get('client_secret'),
            'state': state,
            'code': code
        }

        github_access_token_url = github_conf.get('access_token_url')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        json_body = json.dumps(json_params)

        res = yield httpclient.fetch(github_access_token_url, method='POST', headers=headers, body=json_body)
        json_res = json.loads(res.body)
        raise gen.Return(json_res.get('access_token'))
