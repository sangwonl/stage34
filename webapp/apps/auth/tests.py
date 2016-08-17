from modules.tests import HttpTestCase


class GithubAuthTestCase(HttpTestCase):
    def setUp(self):
        super(GithubAuthTestCase, self).setUp()

    def tearDown(self):
        super(GithubAuthTestCase, self).tearDown()

    def test_hello_world(self):
        result = self.req(url='/auth/github_auth_url', method='GET')
        self.assertTrue('https://github.com/login/oauth/authorize' in result['data']['authorize_url'])
