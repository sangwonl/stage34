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

    # add new deploy key to the repository
    deploy_keys = github_agent.get_deploy_keys(repo)
    deploy_key = None
    for k in deploy_keys:
        if k['title'] == settings.DEPLOY_KEY_TITLE:
            deploy_key = k
            break

    if not deploy_key:
        deploy_key = github_agent.add_deploy_key(
            repo, settings.DEPLOY_KEY_TITLE, settings.DEPLOY_KEY)

    # skip if pub key is already registered
    if not deploy_key or 'errors' in deploy_key:
        if [e for e in deploy_key['errors'] if e['message'] != 'key is already in use']:
            return 'failed to add new deploy key'

    # clone the repository on the directory
    with lcd(settings.REPOSITORY_HOME):
        local('git clone -b {} git@github.com:{}.git {}'.format(branch, repo, str(stage_id)))

