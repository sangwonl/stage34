from __future__ import absolute_import

from celery import shared_task

from api.models.resources import Stage

from libs.backends.provision import DockerComposeLocal


def _udpate_stage_status(stage_id, status):
    Stage.objects.filter(id=stage_id).update(status=status)


def _get_stage_by_id(stage_id):
    return Stage.objects.filter(id=stage_id).first()


@shared_task(queue='q_default')
def task_provision_stage(github_access_key, stage_id, repo, branch, run_on_create):
    # get proper provision backend
    provision_backend = DockerComposeLocal(stage_id, repo, branch, github_access_key)

    # clone the repository on the directory
    result = provision_backend.clone_repository()
    if not result:
        _udpate_stage_status(stage_id, 'paused')
        return 'error'

    # load docker compose file
    result = provision_backend.load_compose_file()
    if not result:
        _udpate_stage_status(stage_id, 'paused')
        return 'error'

    # write docker provision conf
    result = provision_backend.prepare_provision_conf()
    if not result:
        _udpate_stage_status(stage_id, 'paused')
        return 'error'

    # skip running containers updating stage status to paused if not run_on_create 
    if not run_on_create:
        _udpate_stage_status(stage_id, 'paused')
        return 'ok'

    # docker compose up
    result = provision_backend.up()
    if not result:
        _udpate_stage_status(stage_id, 'paused')
        return 'error'

    # update stage status and connect info
    _udpate_stage_status(stage_id, 'running')
    return 'ok'


@shared_task(queue='q_default')
def task_change_stage_status(github_access_key, stage_id, new_status):
    if new_status not in ('running', 'paused'):
        return 'error'

    stage = _get_stage_by_id(stage_id)
    if not stage:
        return 'error'

    # get proper provision backend
    provision_backend = DockerComposeLocal(stage_id, stage.repo, stage.branch, github_access_key)

    # load docker compose file
    result = provision_backend.load_compose_file()
    if not result:
        _udpate_stage_status(stage_id, 'paused')
        return 'error'

    # start or stop containers accoding to `action`
    result = False
    if new_status == 'running':
        result = provision_backend.start()
    elif new_status == 'paused':
        result = provision_backend.stop()

    # update stage status
    _udpate_stage_status(stage_id, new_status)
    return 'ok'
 