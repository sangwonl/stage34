from django.conf import settings
from mako.template import Template

from fabric.api import local
from fabric.context_managers import lcd

from libs.utils.data import merge_dicts

from logs import LogBucket

import errors
import os
import yaml
import json
import shutil
import copy
import uuid
import hashlib


class ProvisionBackend(object):
    def __init__(self, stage_unique_token, repo, branch, repo_access_key):
        self.stage_unique_token = str(stage_unique_token)
        self.entry_container_name = None
        self.repo = repo
        self.branch = branch
        self.repo_access_key = repo_access_key
        self.stage34_data = {}
        self.log_bucket = LogBucket(self.stage_unique_token)

    def clone_repository(self):
        raise NotImplemented

    def pull_repository(self, hash=None):
        raise NotImplemented

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

    def flush_log(self):
        self.log_bucket.flush()


class DockerComposeLocal(ProvisionBackend):
    def __init__(self, *args):
        super(DockerComposeLocal, self).__init__(*args)

    def _get_repo_dir(self):
        return os.path.join(settings.STAGE_REPO_HOME, self.stage_unique_token)

    def _get_repo_based_path(self, filepath):
        repo_home = self._get_repo_dir()
        return os.path.join(repo_home, filepath)

    def _hash_container_name(self, container_name):
        m = hashlib.md5()
        m.update(self.stage_unique_token + self.repo + self.branch + container_name)
        return 'stage34-{}'.format(m.hexdigest()[:10])

    def _makeup_container_names(self, service_data):
        names = {}
        for svc_name, svc_data in service_data['services'].iteritems():
            names.update({svc_name: self._hash_container_name(svc_name)})
        return names

    def _mangle_container_names(self, service_data):
        network_name = settings.DOCKER_NETWORK_BRIDGE
        entry_name = service_data['stage34']['entry']
        del service_data['stage34']

        # container name table
        container_name_table = self._makeup_container_names(service_data)
        for svc_name, svc_data in service_data['services'].iteritems():
            mangled_name = container_name_table.get(svc_name)
            svc_data.update({
                'container_name': mangled_name,
                'networks': [network_name],
                'restart': 'unless-stopped'
            })

            if entry_name == svc_name:
                svc_data.update({'image': mangled_name})

    def _add_network_tier(self, service_data):
        network_name = settings.DOCKER_NETWORK_BRIDGE
        service_data.update({'networks': {
            network_name: {'external': {'name': network_name}}}})

    def _prepare_provision_conf(self):
        # prepare compose data excluding stage34
        service_data = copy.deepcopy(self.stage34_data)

        # container name mangling
        self._mangle_container_names(service_data)

        # add network tier
        self._add_network_tier(service_data)

        # docker-compose.temp.yml without stage34 item
        temp_compose_path = self._get_repo_based_path(settings.DOCKER_COMPOSE_TEMP_FILE)
        with open(temp_compose_path, 'w') as f:
            yaml.dump(service_data, f, default_flow_style=False)

    def _exec_local(self, cmd, except_cls):
        try:
            self.log_bucket.put(cmd)
            output = local(cmd, capture=True)
        except SystemExit as e:
            output = e.message
            raise except_cls()
        finally:
            self.log_bucket.put(output)
        return output

    def _exec_docker_compose_cmd(self, cmd, *args):
        compose_cmd = '{0} -f {1} {2} {3}'.format(
            settings.DOCKER_COMPOSE_BIN_PATH,
            settings.DOCKER_COMPOSE_TEMP_FILE,
            cmd, ' '.join(args) if args else ''
        )
        self._exec_local(compose_cmd, errors.DockerComposeExecError)

    def _docker_inspect(self, container_name):
        docker_inspect_cmd = '{0} inspect {1}'.format(settings.DOCKER_BIN_PATH, container_name) 
        output = self._exec_local(docker_inspect_cmd, errors.DockerInspectExecError)
        return json.loads(output)

    def _get_stage_host_and_port(self, container_name):
        container_info = self._docker_inspect(container_name)
        container_ports = container_info[0]['NetworkSettings']['Ports']
        port_proto = container_ports.keys()[0]

        stage_sub = self.stage_unique_token
        stage_host = settings.STAGE34_HOST
        stage_port = port_proto.split('/')[0]
        return stage_sub, stage_host, stage_port

    def _put_stage_host_local(self, stage_sub, stage_host):
        cmd = "sudo {0} '127.0.0.1    {1}.{2}'".format(settings.ETC_HOSTS_UPDATER_PATH, stage_sub, stage_host)
        self._exec_local(cmd, errors.UpdateLocalHostError)

    def _add_nginx_conf(self, stage_sub, stage_host, stage_port, container_name):
        nginx_templ_path = os.path.join(settings.NGINX_STAGE_TEMPL_DIR, settings.NGINX_STAGE_TEMPL)
        with open(nginx_templ_path, 'r') as f:
            nginx_templ = f.read()

        stage_nginx_conf = Template(nginx_templ).render(
            stage_sub=stage_sub,
            stage_host=stage_host,
            container_host=container_name,
            container_port=stage_port
        )

        nginx_conf_path = os.path.join(settings.NGINX_CONF_PATH, '{}.conf'.format(container_name))
        with open(nginx_conf_path, 'w') as f:
            f.write(stage_nginx_conf)

    def _del_nginx_conf(self, container_name):
        nginx_conf_path = os.path.join(settings.NGINX_CONF_PATH, '{}.conf'.format(container_name))
        if os.path.exists(nginx_conf_path):
            os.remove(nginx_conf_path) 

    def _reload_nginx_conf(self):
        with lcd(settings.PROJECT_DIR):
            cmd = 'docker kill -s HUP {}'.format(settings.NGINX_CONTAINER_NAME)
            self._exec_local(cmd, errors.NginxReloadError)

    def _prepare_nginx_proxy(self, container_name):
        # inpect host port and stage host name
        stage_sub, stage_host, stage_port = self._get_stage_host_and_port(container_name)
        self.log_bucket.put('stage: sub({}), host({}), port({})'.format(stage_sub, stage_host, stage_port))

        # add a nginx conf with proxy pass to the host port and reload nginx
        self._add_nginx_conf(stage_sub, stage_host, stage_port, container_name)
        self.log_bucket.put('added stage nginx config file')

        self._reload_nginx_conf()
        self.log_bucket.put('nginx service reloaded')

    def _disable_nginx_proxy(self, container_name):
        # delete the nginx conf and reload nginx
        self._del_nginx_conf(container_name)
        self.log_bucket.put('deleted stage nginx config file')

        self._reload_nginx_conf()
        self.log_bucket.put('nginx service reloaded')

    def _load_yaml(self, yaml_path):
        yaml_data = None
        with open(yaml_path, 'r') as f:
            try:
                yaml_data = yaml.load(f)
                output = 'loaded successfully'
            except yaml.YAMLError as e:
                output = e.message
                raise errors.InvalidStageConfigError()
            finally:
                self.log_bucket.put(output)
        return yaml_data

    def _load_stage34_svc_file(self):
        # find stage34-services.yml, if not then error
        stage34_compose_path = self._get_repo_based_path(settings.DOCKER_COMPOSE_STAGE34_FILE)
        if not os.path.exists(stage34_compose_path):
            self.log_bucket.put('no such stage34 config file: {}'.format(stage34_compose_path))
            raise errors.StageConfigNotFoundError()
        return self._load_yaml(stage34_compose_path)

    def clone_repository(self):
        self.log_bucket.put('# Git cloning repository...', header=True)

        repo_url = 'https://{0}@github.com/{1}.git'.format(self.repo_access_key, self.repo)
        with lcd(settings.STAGE_REPO_HOME):
            cmd = 'git clone -b {0} {1} {2}'.format(self.branch, repo_url, self.stage_unique_token)
            self._exec_local(cmd, errors.GitRepoCloneError)

    def pull_repository(self, commit_hash=None):
        self.log_bucket.put('# Pulling repository...', header=True)

        repo_home = self._get_repo_dir()
        with lcd(repo_home):
            self.log_bucket.put('repo home: {0}'.format(repo_home))
            cmd = 'git fetch origin {0}'.format(self.branch)
            self._exec_local(cmd, errors.GitRepoPullError)

            target = 'origin/{0}'.format(self.branch) if commit_hash is None else commit_hash
            cmd = 'git reset --hard {0}'.format(target)
            self._exec_local(cmd, errors.GitRepoPullError)

    def load_compose_file(self):
        self.log_bucket.put('# Loading stage34 service config file...', header=True)

        # load stage34 service file
        self.stage34_data = self._load_stage34_svc_file()

        # find stage34.entry app in compose data, if not then error
        if 'stage34' not in self.stage34_data:
            self.log_bucket.put('invalid config data: {}'.format(self.stage34_data))
            raise errors.InvalidStageConfigError()

        # entry hashed container name
        entry_name = self.stage34_data['stage34']['entry']
        self.entry_container_name = self._hash_container_name(entry_name)

    def up(self, recreate=False):
        self.log_bucket.put('# Provisioning stage service...', header=True)

        # write docker provision conf
        self._prepare_provision_conf()
        self.log_bucket.put('prepared temp provision config file')

        # docker compose up
        repo_home = self._get_repo_dir()
        with lcd(repo_home): 
            args = ['-d', '--build']
            if recreate:
                args.append('--no-recreate')
            self._exec_docker_compose_cmd('up', *args)

        # prepare nginx proxy pass
        self._prepare_nginx_proxy(self.entry_container_name)
        self.log_bucket.put('nginx proxy is ready')

    def down(self):
        self.log_bucket.put('# Down the provisioned stage service...', header=True)

        # down docker compose
        repo_home = self._get_repo_dir()
        with lcd(repo_home):
            args = ['--rmi', 'all']
            self._exec_docker_compose_cmd('down', *args)

        # delete repo
        if os.path.exists(repo_home):
            shutil.rmtree(repo_home)
            self.log_bucket.put('deleted repository')
        else:
            self.log_bucket.put('skipped deleting repository as not exist')

        # delete nginx proxy conf and reload
        self._disable_nginx_proxy(self.entry_container_name)
        self.log_bucket.put('nginx proxy is disabled')

    def start(self):
        self.log_bucket.put('# Start the provisioned stage service...', header=True)

        repo_home = self._get_repo_dir()
        with lcd(repo_home): 
            self._exec_docker_compose_cmd('start')

        # prepare nginx proxy pass
        self._prepare_nginx_proxy(self.entry_container_name)
        self.log_bucket.put('nginx proxy is ready')

    def stop(self):
        self.log_bucket.put('# Stop the provisioned stage service...', header=True)

        repo_home = self._get_repo_dir()
        with lcd(repo_home): 
            self._exec_docker_compose_cmd('stop')

        # delete nginx proxy conf and reload
        self._disable_nginx_proxy(self.entry_container_name)
        self.log_bucket.put('nginx proxy is disabled')
