from __future__ import absolute_import

from celery import shared_task
from django.conf import settings
from mako.template import Template

from fabric.api import local
from fabric.context_managers import lcd

from libs.utils.github import GithubAgent
from libs.utils.data import merge_dicts

import os
import yaml
import json


@shared_task(queue='q_default')
def task_provision_stage(github_access_key, stage_id, repo, branch):
    github_agent = GithubAgent(github_access_key)

    # clone the repository on the directory
    with lcd(settings.REPOSITORY_HOME):
        local('git clone -b {0} https://{1}@github.com/{2}.git {3}'.format(branch, github_access_key, repo, stage_id))

    compose_data = {}

    # find docker-compose.stage34.yml, if not then error
    repo_home = os.path.join(settings.REPOSITORY_HOME, stage_id)
    stage34_compose_path = os.path.join(repo_home, settings.DOCKER_COMPOSE_STAGE34_FILE)
    if not os.path.exists(stage34_compose_path):
        return 'error'

    with open(stage34_compose_path, 'r') as f:
        try:
            stage34_compose_data = yaml.load(f)
            compose_data = stage34_compose_data
        except yaml.YAMLError as e:
            return e

    # find docker-compose.yml and merge with stage34 compose data, if not then skip
    default_compose_path = os.path.join(repo_home, settings.DOCKER_COMPOSE_DEFAULT_FILE)
    if os.path.exists(default_compose_path):
        with open(default_compose_path, 'r') as f:
            try:
                def_compose_data = yaml.load(f)
                compose_data = merge_dicts(def_compose_data, stage34_compose_data)
            except yaml.YAMLError as e:
                return e

    # find stage34.entry app in compose data, if not then error
    if 'stage34' not in compose_data or 'entry' not in compose_data['stage34']:
        return 'error'

    entry_name = compose_data['stage34']['entry']
    del compose_data['stage34']

    # write docker-compose.temp.yml without stage34 item
    temp_compose_path = os.path.join(repo_home, settings.DOCKER_COMPOSE_TEMP_FILE)
    with open(temp_compose_path, 'w') as f:
        yaml.dump(compose_data, f, default_flow_style=False)

    # run docker compose with docker-compose.temp.yml
    with lcd(repo_home):
        local('{0} -f {1} up -d'.format(settings.DOCKER_COMPOSE_BIN_PATH, settings.DOCKER_COMPOSE_TEMP_FILE))

    # inpect host port of the entry container (full name is combined dir + app name + numbering)
    entry_container_name = '{0}_{1}_1'.format(stage_id, entry_name)
    out = local('{0} inspect {1}'.format(settings.DOCKER_BIN_PATH, entry_container_name), capture=True)
    container_info = json.loads(out)
    host_port = container_info[0]['NetworkSettings']['Ports'].values()[0][0]['HostPort']

    # add a nginx conf with proxy pass to the host port
    nginx_templ_path = os.path.join(settings.WEBAPP_DIR, 'worker', 'tasks', 'templates', 'stage_nginx.conf')
    with open(nginx_templ_path, 'r') as f:
        nginx_templ = f.read()

    stage_nginx_conf = Template(nginx_templ).render(
        stage_id=stage_id,
        stage34_host=settings.STAGE34_HOST,
        docker_host_port=host_port
    )

    nginx_conf_path = os.path.join(settings.NGINX_CONF_PATH, '{}.conf'.format(entry_container_name))
    with open(nginx_conf_path, 'w') as f:
        f.write(stage_nginx_conf)

    # reload nginx
    with lcd(settings.PROJECT_DIR):
        local('{0} -p nginx -c nginx.conf -s reload'.format(settings.NGINX_BIN_PATH))

    # update stage status and connect info
    pass

