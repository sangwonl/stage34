from django.views import View
from django.conf import settings
from django.core import serializers
from django.forms import model_to_dict

from api.helpers.mixins import AuthRequiredMixin
from api.helpers.http.jsend import JSENDSuccess, JSENDError
from api.models.resources import Membership, Stage

import json
import jwt


RES_FIELDS = ['id', 'title', 'endpoint', 'status', 'repo', 'branch', 'commits', 'created_ts']


class StageRootHandler(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stages_qs = Stage.objects.filter(org=org)
        stages = [model_to_dict(s, fields=RES_FIELDS) for s in stages_qs]
        return JSENDSuccess(status_code=200, data=stages)

    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body)
        title = json_body.get('title')
        repo = json_body.get('repo')
        branch = json_body.get('branch')

        if not (title and repo and branch):
            return JSENDError(status_code=400, msg='invalid stage info')

        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stage = Stage.objects.create(org=org, title=title, repo=repo, branch=branch)
        stage_dict = model_to_dict(stage, fields=RES_FIELDS)
        return JSENDSuccess(status_code=200, data=stage_dict)
