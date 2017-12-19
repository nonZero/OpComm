# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from contextlib import contextmanager

from fabric.api import *
from fabric.contrib.files import upload_template


@contextmanager
def virtualenv(path):
    with cd(path):
        with prefix(env.venv_command):
            yield


@task
def upgrade_pip():
    with virtualenv(env.code_dir):
        run("pip install --upgrade pip", pty=False)


@task
def git_log():
    with virtualenv(env.code_dir):
        run("git log -n 1")


@task
def freeze():
    with virtualenv(env.code_dir):
        run("pip freeze")


@task
def reload_app():
    run("sudo kill -HUP `cat %s`" % env.pidfile)


def workers(cmd):
    sudo("supervisorctl {} oc_celery".format(cmd))


@task
def stop_workers():
    workers("stop")


@task
def start_workers():
    workers("start")


@task
def deploy(restart=True, quick=False, branch=None):
    if restart:
        stop_workers()
    with virtualenv(env.code_dir):
        run("git pull", pty=False)
        if not quick:
            run("pip install -r requirements.txt", pty=False)
            run("python manage.py migrate --noinput")
        run("python manage.py collectstatic --noinput")
        run("git log -n 1 --format=\"%ai %h\" > collected-static/version.txt")
        run("git log -n 1 > collected-static/version-full.txt")
        run('git log -n 1 --format="%h" > oc/static_version.txt')
    if restart:
        reload_app()
        start_workers()


@task
def quickdeploy():
    deploy(True, True)


@task
def clone_project():
    run("git clone %s %s" % (env.clone_url, env.code_dir), pty=False)


@task
def create_venv():
    run("virtualenv {} --prompt='({}) '".format(env.venv_dir, env.user))


@task
def create_prod_local_settings():
    ctx = {}
    ctx['admins'] = '''(
                    ('Yaniv', 'yanivmirel@gmail.com'),
            )
            '''
    ctx['allowed_host'] = "www.opencommittee.co.il"
    ctx['use_imap'] = True
    ctx['is_ssl'] = True
    ctx['host_url'] = "https://www.opencommittee.co.il"

    create_local_settings(ctx)


def create_local_settings(ctx):
    with cd(env.code_dir):
        ctx.update({
            'webuser': env.webuser,
            'host': env.vhost,
        })
        upload_template('conf/prod_settings.py.template',
                        env.code_dir + 'opencommittee/local_settings.py',
                        ctx,
                        use_jinja=True)


@task
def reindex(rebuild=False):
    """Updates/rebuilds haystack search indexes for project"""
    cmd = "rebuild_index --noinput" if rebuild else "update_index"
    with virtualenv(env.code_dir):
        run("python manage.py {}".format(cmd))


@task
def createsuperuser():
    with virtualenv(env.code_dir):
        run("python manage.py createsuperuser")


@task
def del_pyc():
    with cd(env.code_dir):
        run("find . -name '*.pyc' -delete")


@task
def m(params):
    with virtualenv(env.code_dir):
        run("python manage.py {}".format(params))


@task
def find_user(sessionid):
    m("print_user_for_session2 {}".format(sessionid))
