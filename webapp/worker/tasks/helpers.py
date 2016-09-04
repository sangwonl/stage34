from django.conf import settings
from mako.template import Template

from fabric.api import local
from fabric.context_managers import lcd

from libs.utils.data import merge_dicts

import os
import yaml
import json


class ProvisionBackened(object):
    def __init__(self, stage_unique_token, repo, branch, repo_access_key):
        self.stage_unique_token = str(stage_unique_token)
        self.repo = repo
        self.branch = branch
        self.repo_access_key = repo_access_key
        self.compose_data = {}
        self.stage34_data = {}

    def _get_repo_dir(self):
        return os.path.join(settings.STORAGE_HOME, self.stage_unique_token)

    def clone_repository(self):
        repo_url = 'https://{0}@github.com/{1}.git'.format(self.repo_access_key, self.repo)
        with lcd(settings.STORAGE_HOME):
            local('git clone -b {0} {1} {2}'.format(self.branch, repo_url, self.stage_unique_token))
        return True

    def load_compose_file(self):
        raise NotImplemented

    def prepare_provision_conf(self):
        raise NotImplemented

    def up(self, recreate=False):
        raise NotImplemented

    def down(self):
        raise NotImplemented

    def start(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented


class DockerComposeLocal(ProvisionBackened):
    def _get_docker_compose_cmd(self):
        return '{0} -f {1}'.format(settings.DOCKER_COMPOSE_BIN_PATH, settings.DOCKER_COMPOSE_TEMP_FILE)

    def _docker_compose_up(self, recreate):
        compose_cmd = self._get_docker_compose_cmd()
        recreate_opt = '' if recreate else '--no-recreate'
        local('{0} up {1} -d'.format(compose_cmd, recreate_opt))

    def _docker_inspect(self, container_name):
        docker_inspect_cmd = '{0} inspect {1}'.format(settings.DOCKER_BIN_PATH, container_name) 
        out = local(docker_inspect_cmd, capture=True)
        return json.loads(out)

    def _add_and_reload_nginx_conf(self, stage_host, host_port, container_name):
        nginx_templ_path = os.path.join(settings.WEBAPP_DIR, 'worker', 'tasks', 'templates', 'stage_nginx.conf')
        with open(nginx_templ_path, 'r') as f:
            nginx_templ = f.read()

        stage_nginx_conf = Template(nginx_templ).render(
            stage_host=stage_host,
            docker_host_port=host_port
        )

        nginx_conf_path = os.path.join(settings.NGINX_CONF_PATH, '{}.conf'.format(container_name))
        with open(nginx_conf_path, 'w') as f:
            f.write(stage_nginx_conf)

        with lcd(settings.PROJECT_DIR):
            local('{0} -p nginx -c nginx.conf -s reload'.format(settings.NGINX_BIN_PATH))

    def _put_stage_host_local(self, stage_host):
        local("sudo {0} '127.0.0.1    {1}'".format(settings.ETC_HOSTS_UPDATER_PATH, stage_host))

    def load_compose_file(self):
        # find docker-compose.stage34.yml, if not then error
        repo_home = self._get_repo_dir()
        stage34_compose_path = os.path.join(repo_home, settings.DOCKER_COMPOSE_STAGE34_FILE)
        if not os.path.exists(stage34_compose_path):
            return False

        with open(stage34_compose_path, 'r') as f:
            try:
                stage34_compose_data = yaml.load(f)
                self.compose_data = stage34_compose_data
            except yaml.YAMLError as e:
                return False

        # find docker-compose.yml and merge with stage34 compose data, if not then skip
        default_compose_path = os.path.join(repo_home, settings.DOCKER_COMPOSE_DEFAULT_FILE)
        if os.path.exists(default_compose_path):
            with open(default_compose_path, 'r') as f:
                try:
                    def_compose_data = yaml.load(f)
                    self.compose_data = merge_dicts(def_compose_data, stage34_compose_data)
                except yaml.YAMLError as e:
                    return False

        # find stage34.entry app in compose data, if not then error
        if ('stage34' not in self.compose_data or
            'entry' not in self.compose_data['stage34']):
            return False

        self.stage34_data = self.compose_data['stage34']
        del self.compose_data['stage34']
        return True

    def prepare_provision_conf(self):
        # docker-compose.temp.yml without stage34 item
        repo_home = self._get_repo_dir()
        temp_compose_path = os.path.join(repo_home, settings.DOCKER_COMPOSE_TEMP_FILE)
        with open(temp_compose_path, 'w') as f:
            yaml.dump(self.compose_data, f, default_flow_style=False)
        return True

    def up(self, recreate=False):
        # docker compose up
        repo_home = self._get_repo_dir()
        with lcd(repo_home): 
            self._docker_compose_up(recreate)

        # inpect host port of the entry container (full name is combined dir + app name + numbering)
        entry_name = self.stage34_data['entry']
        entry_container_name = '{0}_{1}_1'.format(self.stage_unique_token, entry_name)
        container_info = self._docker_inspect(entry_container_name)
        host_port = container_info[0]['NetworkSettings']['Ports'].values()[0][0]['HostPort']

        # add stage host into /etc/hosts
        stage_host = '{0}.{1}'.format(self.stage_unique_token, settings.STAGE34_HOST)
        self._put_stage_host_local(stage_host)

        # add a nginx conf with proxy pass to the host port and reload nginx
        self._add_and_reload_nginx_conf(stage_host, host_port, entry_container_name)

        return True

    def down(self):
        raise NotImplemented

    def start(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented
