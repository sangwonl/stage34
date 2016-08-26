from __future__ import absolute_import

from celery import shared_task

from django.conf import settings

from libs.utils.github import GithubAgent


@shared_task(queue='q_default')
def task_provision_stage(github_access_key, repo, branch):
    github_agent = GithubAgent(github_access_key)
    deploy_keys = github_agent.get_deploy_keys(repo)

    deploy_key = None
    for k in deploy_keys:
        if k['title'] == settings.DEPLOY_KEY_TITLE:
            deploy_key = k
            break

    if not deploy_key:
        deploy_key = github_agent.add_deploy_key(
            repo, settings.DEPLOY_KEY_TITLE, settings.DEPLOY_KEY)

    if not deploy_key or 'errors' in deploy_key:
        if deploy_key['errors']['message'] != 'key is already in use':
            return 'failed to add new deploy key'

    # create a unique directory named including stage id

    # clone the repository on the directory
