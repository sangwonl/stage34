from django.conf import settings

import requests
import uuid
import urllib
import json


class GithubAgent(object):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def _get_api_base(self):
        return settings.GITHUB_API.get('api_base_url')

    def _get_api_hdrs(self):
        return {'Authorization': 'token {0}'.format(self.access_token)}

    def get_authorize_url(self):
        query_params = {
            'redirect_uri': settings.GITHUB_API.get('redirect_uri'),
            'client_id': settings.GITHUB_API.get('client_id'),
            'scope': settings.GITHUB_API.get('scope'),
            'state': str(uuid.uuid4().hex),
            'response_type': 'code'
        }

        github_auth_base_url = settings.GITHUB_API.get('authorize_url')
        urlencoded_query_parms = urllib.urlencode(query_params)
        return '{0}?{1}'.format(github_auth_base_url, urlencoded_query_parms)

    def request_access_token(self, state, code):
        res = requests.post(
            url=settings.GITHUB_API.get('access_token_url'),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
            json={
                'client_id': settings.GITHUB_API.get('client_id'),
                'client_secret': settings.GITHUB_API.get('client_secret'),
                'state': state,
                'code': code
            }
        )

        json_res = res.json()
        return json_res.get('access_token')

    def get_primary_email(self):
        res = requests.get(
            url='{0}/user/emails'.format(self._get_api_base()),
            headers=self._get_api_hdrs()
        )

        primary_email = None
        json_res = res.json()
        for email_obj in json_res:
            if email_obj.get('primary'):
                primary_email = email_obj.get('email')
                break

        return primary_email

    def get_deploy_keys(self, repo):
        res = requests.get(
            url='{0}/repos/{1}/keys'.format(self._get_api_base(), repo),
            headers=self._get_api_hdrs()
        )
        return res.json()

    def add_deploy_key(self, repo, key_title, key_file):
        key = ''
        with open(key_file, 'rt') as key_f:
            key = key_f.read()

        res = requests.post(
            url='{}/repos/{}/keys'.format(self._get_api_base(), repo),
            headers=self._get_api_hdrs(),
            json={'title': key_title, 'key': key, 'read_only': True}
        )
        return res.json()
