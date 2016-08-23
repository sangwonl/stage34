from django.views import View
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core import serializers
from django.forms import model_to_dict

from api.helpers.http.jsend import JSENDSuccess, JSENDError
from api.helpers.agents.github import GithubAgent
from api.models import User

import json
import jwt


class GithubAuthUrlHandler(View):
    def get(self, request, *args, **kwargs):
        auth_url = GithubAgent().get_authorize_url()
        return JSENDSuccess(status_code=200, data={'authorize_url': auth_url})


class GithubCallbackHandler(View):
    def get(self, request, *args, **kwargs):
        state = request.GET.get('state', None)
        code = request.GET.get('code', None)
        access_token = GithubAgent().request_access_token(state, code)

        res = HttpResponseRedirect('/login')
        res.set_cookie('github-access-token', access_token)
        return res


class LoginHandler(View):
    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body)
        email = json_body.get('email')
        access_token = json_body.get('access_token')

        # query email by access token and check if it is matched
        primary_email = GithubAgent(access_token).get_primary_email()
        if not primary_email or primary_email != email:
            return JSENDError(status_code=401, msg='not matched email')

        # get or create user
        user, created = User.objects.get_or_create(email=email)

        # create jwt
        payload = {'uid': user.id, 'email': email, 'access_token': access_token}
        token = jwt.encode(payload=payload, key=settings.JWT_SECRET)

        # save jwt on user
        user.token = token
        user.save()

        # serialize
        user_dict = model_to_dict(user, fields=['id', 'email', 'token'])
        return JSENDSuccess(status_code=200, data=user_dict)
