from django.views import View
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core import serializers
from django.forms import model_to_dict

from api.helpers.http.jsend import JSENDSuccess, JSENDError
from api.helpers.agents.github import GithubAgent
from api.models import User
from api.models.resources import Organization, Membership

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

        # get or create an user with jwt token
        user, created = self.get_or_create_user_with_token(primary_email, access_token)

        # create singleton organization and membership for the first time
        if created:
            self.add_user_to_singleton_organization(user)

        # serialize
        user_dict = model_to_dict(user, fields=['id', 'email', 'token'])
        return JSENDSuccess(status_code=200, data=user_dict)

    def get_or_create_user_with_token(self, email, access_token):
        user, created = User.objects.get_or_create(email=email)
        payload = {'uid': user.id, 'email': email, 'access_token': access_token}
        user.token = jwt.encode(payload=payload, key=settings.JWT_SECRET)
        user.save()
        return user, created

    def add_user_to_singleton_organization(self, user):
        singleton_org = Organization.objects.first()
        if not singleton_org:
            def_org_name = settings.DEFAULT_ORG_NAME
            singleton_org = Organization.objects.create(name=def_org_name)

        # get or create a membership of user and org
        Membership.objects.get_or_create(user=user, organization=singleton_org)
