from tornado import gen

from modules.http.handlers import BaseHandler, AsyncBaseHandler
from modules.http import JSENDSuccess, JSENDError
from modules.agents.github import GithubAgent

from conf import settings
from models import db, User

import jwt


class GithubAuthUrlHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        auth_url = GithubAgent().get_authorize_url()
        res = JSENDSuccess(status_code=200, data={'authorize_url': auth_url})
        raise gen.Return(res)


class GithubCallbackHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_get(self, *args, **kwargs):
        state = self.get_argument('state', None)
        code = self.get_argument('code', None)
        access_token = yield GithubAgent().request_access_token(state, code)
        self.set_cookie('github-access-token', access_token)
        self.redirect('/login')


class LoginHandler(AsyncBaseHandler):
    @gen.coroutine
    def do_post(self, *args, **kwargs):
        json_body = self.get_json_body()
        email = json_body.get('email')
        access_token = json_body.get('access_token')

        # query email by access token and check if it is matched
        primary_email = yield GithubAgent(access_token).get_primary_email()
        if not primary_email or primary_email != email:
            raise gen.Return(JSENDError(status_code=401, msg='not matched email'))

        # get or create user
        user = db.query(User).filter_by(email=email).first()
        if not user:
            user = User(email=email)

        # create jwt
        secret = settings.get('jwt_secret')
        token = jwt.encode(payload={'email': email, 'access_token': access_token}, key=secret)

        # save jwt on user
        user.jwt = token
        db.add(user)
        db.commit()

        res = JSENDSuccess(status_code=200, data=user.json())
        raise gen.Return(res)
