from django.views import View
from django.conf import settings
from django.core import serializers
from django.forms import model_to_dict

from api.helpers.mixins import AuthRequiredMixin
from api.helpers.http.jsend import JSENDSuccess, JSENDError
from api.models.resources import Membership, Stage

from worker.tasks.deployment import task_provision_stage

import json
import jwt


SERIALIZE_FIELDS = [
    'id',
    'title',
    'endpoint',
    'status',
    'repo',
    'default_branch',
    'branch',
    'created_at'
]


class StageRootHandler(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stages_qs = Stage.objects.filter(org=org)
        stages = [model_to_dict(s, fields=SERIALIZE_FIELDS) for s in stages_qs]
        return JSENDSuccess(status_code=200, data=stages)

    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body)
        title = json_body.get('title')
        repo = json_body.get('repo')
        default_branch= json_body.get('default_branch')
        branch= json_body.get('branch')

        if not (title and repo and default_branch and branch):
            return JSENDError(status_code=400, msg='invalid stage info')

        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stage = Stage.objects.create(
            org=org,
            title=title,
            repo=repo,
            default_branch=default_branch,
            branch=branch
        )

        github_access_key = request.user.jwt_payload.get('access_token')
        task_provision_stage.apply_async(args=[github_access_key, stage.id, repo, branch])

        stage_dict = model_to_dict(stage, fields=SERIALIZE_FIELDS)
        return JSENDSuccess(status_code=200, data=stage_dict)


class StageDetailHandler(AuthRequiredMixin, View):
    def get_stage(self, org, stage_id):
        try:
            stage = Stage.objects.get(org=org, id=stage_id)
        except Stage.DoesNotExist:
            return None
        return stage

    def get(self, request, stage_id, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stage = self.get_stage(org, stage_id)
        if not stage:
            return JSENDError(status_code=404, msg='stage not found')

        stage_dict = model_to_dict(stage, fields=SERIALIZE_FIELDS)
        return JSENDSuccess(status_code=200, data=stage_dict)

    def put(self, request, stage_id, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stage = self.get_stage(org, stage_id)
        if not stage:
            return JSENDError(status_code=404, msg='stage not found')

        json_body = json.loads(request.body)
        stage.title = json_body.get('title', stage.title)
        stage.repo = json_body.get('repo', stage.repo)
        stage.default_branch = json_body.get('default_branch', stage.default_branch)
        stage.branch = json_body.get('branch', stage.branch)
        stage.status = json_body.get('status', stage.status)
        stage.endpoint = json_body.get('endpoint', stage.endpoint)
        stage.save()

        stage_dict = model_to_dict(stage, fields=SERIALIZE_FIELDS)
        return JSENDSuccess(status_code=204, data=stage_dict)

    def delete(self, request, stage_id, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stage = self.get_stage(org, stage_id)
        if not stage:
            return JSENDError(status_code=404, msg='stage not found')

        stage.delete()

        return JSENDSuccess(status_code=204, data={})