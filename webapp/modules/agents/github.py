from tornado import gen
from conf import settings

from modules.http import client as httpclient

import uuid
import urllib
import json


class GithubAgent(object):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_authorize_url(self):
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

    @gen.coroutine
    def request_access_token(self, state, code):
        github_conf = settings.get('github')
        json_params = {
            'client_id': github_conf.get('client_id'),
            'client_secret': github_conf.get('client_secret'),
            'state': state,
            'code': code
        }

        res = yield httpclient.fetch(
            method='POST',
            url=github_conf.get('access_token_url'),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
            body=json.dumps(json_params)
        )

        json_res = json.loads(res.body)
        raise gen.Return(json_res.get('access_token'))

    @gen.coroutine
    def get_primary_email(self):
        github_conf = settings.get('github')
        github_api_base_url = github_conf.get('api_base_url')

        res = yield httpclient.fetch(
            method='GET',
            url='%s/user/emails' % github_api_base_url,
            headers={'Authorization': 'token %s' % self.access_token}
        )

        primary_email = None
        json_res = json.loads(res.body)
        for email_obj in json_res:
            if email_obj.get('primary'):
                primary_email = email_obj.get('email')
                break

        raise gen.Return(primary_email)
