from __future__ import absolute_import

from celery import shared_task

from api.models.resources import Stage

from libs.backends.provision import DockerComposeLocal


@shared_task(queue='q_default')
def task_provision_stage(github_access_key, stage_id, repo, branch, run_on_create):
    def _udpate_stage_status(status):
        Stage.objects.filter(id=stage_id).update(status=status)

    # get proper provision backend
    provision_backend = DockerComposeLocal(stage_id, repo, branch, github_access_key)

    # clone the repository on the directory
    result = provision_backend.clone_repository()
    if not result:
        _udpate_stage_status('paused')
        return 'error'

    # load docker compose file
    result = provision_backend.load_compose_file()
    if not result:
        _udpate_stage_status('paused')
        return 'error'

    # write docker provision conf
    result = provision_backend.prepare_provision_conf()
    if not result:
        _udpate_stage_status('paused')
        return 'error'

    # skip running containers updating stage status to paused if not run_on_create 
    if not run_on_create:
        _udpate_stage_status('paused')
        return 'ok'

    # docker compose up
    result = provision_backend.up()
    if not result:
        _udpate_stage_status('paused')
        return 'error'

    # update stage status and connect info
    _udpate_stage_status('running')
    return 'ok'


@shared_task(queue='q_default')
def task_change_stage_status(github_access_key, stage_id, action):
    def _udpate_stage_status(status):
        Stage.objects.filter(id=stage_id).update(status=status)

    if action not in ('start', 'stop'):
        return 'error'

    stage = Stage.objects.filter(id=stage_id).first()
    if not stage:
        return 'error'

    # get proper provision backend
    provision_backend = DockerComposeLocal(stage_id, stage.repo, stage.branch, github_access_key)

    # start or stop containers accoding to `action`
    result = False
    new_status = ''
    if action == 'start':
        new_status = 'running'
        result = provision_backend.start()
    elif action == 'stop':
        new_status = 'paused'
        result = provision_backend.stop()

    if not result or not new_status:
        return 'error'

    # update stage status
    _udpate_stage_status(new_status)
 