from __future__ import absolute_import

from celery import shared_task


@shared_task(queue='q_default')
def task_provision_stage(github_access_key, repo, branch):
    print github_access_key, repo, branch
