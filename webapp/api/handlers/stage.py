from django.views import View
from django.conf import settings
from datetime import datetime

from api.helpers.mixins import AuthRequiredMixin
from api.helpers.http.jsend import JSENDSuccess, JSENDError
from api.models.resources import Membership, Stage

from libs.utils.model_ext import model_to_dict

from worker.tasks.deployment import (
    task_provision_stage,
    task_change_stage_status,
    task_delete_stage,
    task_refresh_stage
)

import pytz
import os
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
        branch= json_body.get('branch')
        default_branch= json_body.get('default_branch')
        run_on_create = json_body.get('run_on_create', False)

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
        task_provision_stage.apply_async(args=[github_access_key, stage.id, repo, branch, run_on_create])

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
        json_body = json.loads(request.body)
        new_status = json_body.get('status')
        if not new_status or new_status not in ('running', 'paused'):
            return JSENDError(status_code=400, msg='invalid stage status')

        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stage = self.get_stage(org, stage_id)
        if not stage:
            return JSENDError(status_code=404, msg='stage not found')

        cur_status = stage.status
        if cur_status != new_status:
            github_access_key = request.user.jwt_payload.get('access_token')
            task_change_stage_status.apply_async(args=[github_access_key, stage_id, new_status])
            new_status = 'changing'

        stage.title = json_body.get('title', stage.title)
        stage.repo = json_body.get('repo', stage.repo)
        stage.default_branch = json_body.get('default_branch', stage.default_branch)
        stage.branch = json_body.get('branch', stage.branch)
        stage.status = new_status
        stage.save()

        stage_dict = model_to_dict(stage, fields=SERIALIZE_FIELDS)
        return JSENDSuccess(status_code=204)

    def delete(self, request, stage_id, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stage = self.get_stage(org, stage_id)
        if not stage:
            return JSENDError(status_code=404, msg='stage not found')

        stage.status = 'deleting'
        stage.save()

        github_access_key = request.user.jwt_payload.get('access_token')
        task_delete_stage.apply_async(args=[github_access_key, stage_id])

        return JSENDSuccess(status_code=204)


class StageLogHandler(AuthRequiredMixin, View):
    def get_log_path(self, stage_id):
        return os.path.join(settings.STAGE_REPO_HOME, stage_id, 'output.log')

    def get(self, request, stage_id, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        log_path = self.get_log_path(stage_id) 
        if not os.path.exists(log_path):
            return JSENDError(status_code=404, msg='log file not found')

        log_msgs = []
        with open(log_path, 'rt') as f:
            log_msg = f.read()
            log_msgs = [l for l in log_msg.split('\n') if l]

        ts = os.path.getmtime(log_path)
        tz = pytz.timezone(settings.TIME_ZONE)
        dt = datetime.fromtimestamp(ts, tz=tz)

        log_data = {'log_messages': log_msgs, 'log_time': dt.isoformat()}
        return JSENDSuccess(status_code=200, data=log_data)


class StageRefreshHandler(AuthRequiredMixin, View):
    def get_stage(self, org, stage_id):
        try:
            stage = Stage.objects.get(org=org, id=stage_id)
        except Stage.DoesNotExist:
            return None
        return stage

    def post(self, request, stage_id, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stage = self.get_stage(org, stage_id)
        if not stage:
            return JSENDError(status_code=404, msg='stage not found')

        github_access_key = request.user.jwt_payload.get('access_token')
        task_refresh_stage.apply_async(args=[github_access_key, stage_id])

        stage.status = 'changing'
        stage.save()

        stage_dict = model_to_dict(stage, fields=SERIALIZE_FIELDS)
        return JSENDSuccess(status_code=204)
