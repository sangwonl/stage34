from __future__ import absolute_import

from celery import shared_task

from django.conf import settings
from fabric.api import local
from fabric.context_managers import lcd

from libs.utils.github import GithubAgent

import os


@shared_task(queue='q_default')
def task_provision_stage(github_access_key, stage_id, repo, branch):
    github_agent = GithubAgent(github_access_key)

    # clone the repository on the directory
    with lcd(settings.REPOSITORY_HOME):
        local('git clone -b {0} https://{1}@github.com/{2}.git {3}'.format(branch, github_access_key, repo, stage_id))
