import contextlib
import os
from os.path import relpath, join

import requests
from devtools.management.deploy_phases import registry, Phase
from devtools.management.environments import LocalEnvironment, RemoteEnvironment
from devtools.signals import pre_assets, post_assets, pre_restart, post_restart
from django.conf import settings
from django.core.management import CommandError


@registry.replace
class AssetsPhase(Phase):
    tag = 'assets'
    before = ['static', 'update']
    requires = ['update', 'static', 'restart', 'clean']
    help_message = 'Custom assets builder'
    deploy_message = 'Building frontend'

    @classmethod
    def required_by_change(cls, file_name):
        return 'frontend/' in file_name

    def execute(self, branch=None):
        if isinstance(self.environment, LocalEnvironment):
            self.update_assets_local()
        elif isinstance(self.environment, RemoteEnvironment):
            self.update_assets_remote()
        else:
            raise RuntimeError(f'Unknown environment type {self.environment.__class__}')

    @contextlib.contextmanager
    def prepare_assets_local(self, local_env, deploy_configuration=None):
        env = local_env
        target = str(settings.FRONTEND_DIR.path('build', 'static'))
        with env.operator.cd(str(settings.FRONTEND_DIR)) as operator:
            operator.run('node sonic build')

        dir_list = []
        file_list = []
        for root, dirs, files in os.walk(target, topdown=False):
            for name in dirs:
                dir_list.append((target, join(relpath(root, target), name)))
            for name in files:
                file_list.append((target, join(relpath(root, target), name)))

        yield (dir_list, file_list)

    def update_assets_local(self):
        env = self.environment
        pre_assets.send(env)
        with env.operator.cd(env.deploy_configuration['frontend_dir']) as operator:
            operator.run([
                'node sonic build',
            ])
        post_assets.send(self)

    def update_assets_remote(self):
        env = self.environment
        pre_assets.send(env)

        if any(['/frontend/' in line for line in env.local.get_diff()]):
            raise CommandError("""
                Your local environment has uncommitted changes to frontend, please commit
                them first.
            """)

        commit_hash = env.local.get_current_commit()

        sentry_api_base_url = env.deploy_configuration.get('sentry_api_url')
        sentry_api_token = env.local.get_sentry_api_token()

        if sentry_api_base_url and not sentry_api_token:
            raise CommandError("""
                You have to setup your Sentry API token before you can upload assets.

                Make sure you have a SENTRY_AUTH_TOKEN with project:write in your
                environment or .env-file.
            """)
        elif sentry_api_base_url:
            # Make sure we have a release
            requests.post(
                '{}{}'.format(sentry_api_base_url, 'releases/'),
                headers={
                    'Authorization': 'Bearer {}'.format(sentry_api_token),
                },
                json={'version': commit_hash, },
            )

        with self.prepare_assets_local(env.local) as file_lists:
            dirs, files = file_lists
            env.operator.run('mkdir -p {project_dir}/assets/'.format(
                project_dir=env.deploy_configuration['project_dir']
            ))
            for (root, relpathi) in dirs:
                env.operator.run('mkdir -p {project_dir}/assets/{relpath}'.format(
                    project_dir=env.deploy_configuration['project_dir'],
                    relpath=relpathi,
                ))
            for (root, relpathi,) in files:
                if relpathi == 'webpack-stats.json':
                    env.operator.put(
                        os.path.join(root, relpathi),
                        '{project_dir}/{name}'.format(
                            name=relpathi,
                            project_dir=env.deploy_configuration[
                                'project_dir']
                        ))
                else:
                    env.operator.put(
                        os.path.join(root, relpathi),
                        '{project_dir}/assets/{name}'.format(
                            name=relpathi,
                            project_dir=env.deploy_configuration['project_dir']
                        ))
                    if sentry_api_base_url:
                        # Make upload it to Sentry
                        with open(os.path.join(root, relpathi), 'r') as f:
                            requests.post(
                                '{}{}'.format(
                                    sentry_api_base_url,
                                    'releases/{}/files/'.format(commit_hash)
                                ),
                                headers={
                                    'Authorization': 'Bearer {}'.format(sentry_api_token),
                                },
                                files={'file': f},
                                data={'name': '~{}'.format(
                                    env.get_static_name(f'{relpathi}')
                                )}
                            )

        post_assets.send(env)


# @registry.replace
# class ReloadPhase(Phase):
#     tag = 'restart'
#     after = ['update']
#     help_message = 'Custom reload script'
#     deploy_message = 'Restarting apache'
#
#     def execute(self, branch=None):
#         env = self.environment
#         pre_restart.send(env)
#         with env.operator.cd(env.deploy_configuration['project_dir']) as operator:
#             operator.run(
#                 'sudo /opt/bitnami/ctlscript.sh restart apache',
#             )
#         post_restart.send(env)
