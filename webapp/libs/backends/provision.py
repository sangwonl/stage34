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


class ProvisionBackend(object):
    def __init__(self, stage_unique_token, repo, branch, repo_access_key):
        self.stage_unique_token = str(stage_unique_token)
        self.repo = repo
        self.branch = branch
        self.repo_access_key = repo_access_key
        self.stage34_data = {}
        self.log_bucket = LogBucket(self.stage_unique_token)

    def clone_repository(self):
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
        return os.path.join(settings.STORAGE_HOME, self.stage_unique_token)

    def _prepare_provision_conf(self):
        # prepare compose data excluding stage34
        compose_data = copy.deepcopy(self.stage34_data)
        assert 'stage34' in compose_data
        del compose_data['stage34']

        # docker-compose.temp.yml without stage34 item
        repo_home = self._get_repo_dir()
        temp_compose_path = os.path.join(repo_home, settings.DOCKER_COMPOSE_TEMP_FILE)
        with open(temp_compose_path, 'w') as f:
            yaml.dump(compose_data, f, default_flow_style=False)

    def _exec_docker_compose_cmd(self, cmd, *args):
        compose_cmd = '{0} -f {1} {2} {3}'.format(
            settings.DOCKER_COMPOSE_BIN_PATH,
            settings.DOCKER_COMPOSE_TEMP_FILE,
            cmd, ' '.join(args) if args else ''
        )
        try:
            self.log_bucket.put(compose_cmd)
            output = local(compose_cmd, capture=True)
        except SystemExit as e:
            output = e.message
            raise errors.DockerComposeExecError()
        finally:
            self.log_bucket.put(output)

    def _docker_inspect(self, container_name):
        docker_inspect_cmd = '{0} inspect {1}'.format(settings.DOCKER_BIN_PATH, container_name) 
        try:
            self.log_bucket.put(docker_inspect_cmd)
            output = local(docker_inspect_cmd, capture=True)
        except SystemExit as e:
            output = e.message
            self.log_bucket.put(output)
            raise errors.DockerInspectExecError()
        return json.loads(output)

    def _get_entry_container_name(self):
        # naming of the entry container (stage id + app name + numbering)
        container_name = ''
        if 'stage34' in self.stage34_data:
            entry_name = self.stage34_data['stage34']['entry']
            container_name = '{0}_{1}_1'.format(self.stage_unique_token, entry_name)
        return container_name

    def _get_stage_and_host_endpoint(self, container_name):
        container_info = self._docker_inspect(container_name)
        container_ports = container_info[0]['NetworkSettings']['Ports']
        host_port = None
        for port, detail in container_ports.iteritems():
            if detail and len(detail) == 1:
                host_port = detail[0]['HostPort']
                break

        stage_sub = self.stage_unique_token
        stage_host = settings.STAGE34_HOST
        return stage_sub, stage_host, host_port

    def _put_stage_host_local(self, stage_sub, stage_host):
        cmd = "sudo {0} '127.0.0.1    {1}.{2}'".format(settings.ETC_HOSTS_UPDATER_PATH, stage_sub, stage_host)
        try:
            self.log_bucket.put(cmd)
            output = local(cmd, capture=True)
        except SystemExit as e:
            output = e.message
            raise errors.UpdateLocalHostError()
        finally:
            self.log_bucket.put(output)

    def _add_nginx_conf(self, stage_sub, stage_host, host_port, container_name):
        nginx_templ_path = os.path.join(settings.NGINX_STAGE_TEMPL_DIR, settings.NGINX_STAGE_TEMPL)
        with open(nginx_templ_path, 'r') as f:
            nginx_templ = f.read()

        stage_nginx_conf = Template(nginx_templ).render(
            stage_sub=stage_sub,
            stage_host=stage_host,
            docker_host_port=host_port
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
            cmd = '{0} -p {1} -c nginx.conf -s reload'.format(settings.NGINX_BIN_PATH, settings.NGINX_CONF_PREFIX)
            try:
                self.log_bucket.put(cmd)
                output = local(cmd, capture=True)
            except SystemExit as e:
                output = e.message
                raise errors.NginxReloadError()
            finally:
                self.log_bucket.put(output)

    def _prepare_nginx_proxy(self, container_name):
        # inpect host port and stage host name
        stage_sub, stage_host, host_port = self._get_stage_and_host_endpoint(container_name)
        self.log_bucket.put('endpoints: stage-host({}.{}), host-port({})'.format(stage_sub, stage_host, host_port))

        # add stage host into /etc/hosts
        if settings.ETC_HOSTS_UPDATE:
            self._put_stage_host_local(stage_sub, stage_host)

        # add a nginx conf with proxy pass to the host port and reload nginx
        self._add_nginx_conf(stage_sub, stage_host, host_port, container_name)
        self.log_bucket.put('added stage nginx config file')

        self._reload_nginx_conf()
        self.log_bucket.put('nginx service reloaded')

    def _disable_nginx_proxy(self, container_name):
        # delete the nginx conf and reload nginx
        self._del_nginx_conf(container_name)
        self.log_bucket.put('deleted stage nginx config file')

        self._reload_nginx_conf()
        self.log_bucket.put('nginx service reloaded')

    def clone_repository(self):
        self.log_bucket.put('# Git cloning repository...', header=True)

        repo_url = 'https://{0}@github.com/{1}.git'.format(self.repo_access_key, self.repo)
        with lcd(settings.STORAGE_HOME):
            cmd = 'git clone -b {0} {1} {2}'.format(self.branch, repo_url, self.stage_unique_token)
            try:
                self.log_bucket.put(cmd)
                output = local(cmd, capture=True)
            except SystemExit as e:
                output = e.message
                raise errors.GitRepoCloneError()
            finally:
                self.log_bucket.put(output)

    def load_compose_file(self):
        self.log_bucket.put('# Loading stage34 service config file...', header=True)

        # find stage34-services.yml, if not then error
        repo_home = self._get_repo_dir()
        stage34_compose_path = os.path.join(repo_home, settings.DOCKER_COMPOSE_STAGE34_FILE)
        if not os.path.exists(stage34_compose_path):
            self.log_bucket.put('no such stage34 config file: {}'.format(stage34_compose_path))
            raise errors.StageConfigNotFoundError()

        with open(stage34_compose_path, 'r') as f:
            try:
                self.stage34_data = yaml.load(f)
                output = 'loaded successfully'
            except yaml.YAMLError as e:
                output = e.message
                raise errors.InvalidStageConfigError()
            finally:
                self.log_bucket.put(output)

        # find stage34.entry app in compose data, if not then error
        if 'stage34' not in self.stage34_data:
            self.log_bucket.put('invalid config data: {}'.format(self.stage34_data))
            raise errors.InvalidStageConfigError()

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

        # get entry container name
        entry_container_name = self._get_entry_container_name()  

        # prepare nginx proxy pass
        self._prepare_nginx_proxy(entry_container_name)
        self.log_bucket.put('nginx proxy is ready')

    def down(self):
        self.log_bucket.put('# Down the provisioned stage service...', header=True)

        # delete repo
        repo_home = self._get_repo_dir()
        if os.path.exists(repo_home):
            shutil.rmtree(repo_home)
            self.log_bucket.put('deleted repository')
        else:
            self.log_bucket.put('skipped deleting repository as not exist')

        # get entry container name
        entry_container_name = self._get_entry_container_name()

        # delete nginx proxy conf and reload
        self._disable_nginx_proxy(entry_container_name)
        self.log_bucket.put('nginx proxy is disabled')

        # down docker compose
        with lcd(repo_home):
            self._exec_docker_compose_cmd('down')

    def start(self):
        self.log_bucket.put('# Start the provisioned stage service...', header=True)

        repo_home = self._get_repo_dir()
        with lcd(repo_home): 
            self._exec_docker_compose_cmd('start')

        # get entry container name
        entry_container_name = self._get_entry_container_name()  

        # prepare nginx proxy pass
        self._prepare_nginx_proxy(entry_container_name)
        self.log_bucket.put('nginx proxy is ready')

    def stop(self):
        self.log_bucket.put('# Stop the provisioned stage service...', header=True)

        repo_home = self._get_repo_dir()
        with lcd(repo_home): 
            self._exec_docker_compose_cmd('stop')

        # get entry container name
        entry_container_name = self._get_entry_container_name()  

        # delete nginx proxy conf and reload
        self._disable_nginx_proxy(entry_container_name)
        self.log_bucket.put('nginx proxy is disabled')
