from __future__ import absolute_import

from celery import shared_task

from api.models.resources import Stage

from libs.backends.provision import DockerComposeLocal


def _udpate_stage_status(stage_id, status, is_up=None):
    if is_up is None:
        Stage.objects.filter(id=stage_id).update(status=status)
    else:
        Stage.objects.filter(id=stage_id).update(status=status, is_up=is_up)


def _get_stage_by_id(stage_id):
    return Stage.objects.filter(id=stage_id).first()


def _delete_stage_by_id(stage_id):
    Stage.objects.filter(id=stage_id).delete()


@shared_task(queue='q_default')
def task_provision_stage(github_access_key, stage_id, repo, branch, run_on_create):
    # get proper provision backend
    provision_backend = DockerComposeLocal(stage_id, repo, branch, github_access_key)

    try:
        # clone the repository on the directory
        provision_backend.clone_repository()

        # load docker compose file
        provision_backend.load_compose_file()

        # provisioning if run_on_create is set
        if run_on_create:
            provision_backend.up()

    except Exception as e:
        print e
        _udpate_stage_status(stage_id, 'paused')
        return 'error'
    
    finally:
        provision_backend.flush_log()

    # update stage status and connect info
    is_up = False
    status = 'paused'
    if run_on_create:
        status = 'running'
        is_up = True
    _udpate_stage_status(stage_id, status, is_up)
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

    is_up = None
    try:
        # load docker compose file
        provision_backend.load_compose_file()

        # start or stop containers accoding to `action`
        result = False
        if new_status == 'running':
            if stage.is_up:
                provision_backend.start()
            else:
                provision_backend.up()
                is_up = True
        elif new_status == 'paused':
            provision_backend.stop()

    except Exception as e:
        print e
        _udpate_stage_status(stage_id, 'paused')
        return 'error'

    finally:
        provision_backend.flush_log()

    # update stage status
    _udpate_stage_status(stage_id, new_status, is_up=is_up)
    return 'ok'
 

@shared_task(queue='q_default')
def task_delete_stage(github_access_key, stage_id):
    stage = _get_stage_by_id(stage_id)
    if not stage:
        return 'error'

    if stage.status not in ('paused'):
        return 'error'

    # get proper provision backend
    provision_backend = DockerComposeLocal(stage_id, stage.repo, stage.branch, github_access_key)

    try:
        # load docker compose file
        provision_backend.load_compose_file()

        # tear down stage
        provision_backend.down()

    except Exception as e:
        print e

    finally:
        provision_backend.flush_log()

    # delete stage
    _delete_stage_by_id(stage_id)
    return 'ok'