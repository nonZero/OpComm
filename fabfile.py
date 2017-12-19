import datetime

from fabric.api import *

from fab_tools.server import *
from fab_tools.project import *
from fab_tools import db
assert db
from fab_tools import dev
assert dev
import os.path

PROJ_DIR = os.path.abspath(os.path.dirname(__file__))
CONF_DIR = os.path.abspath(os.path.join(PROJ_DIR, 'conf'))


env.project = "oc"
env.user = "oc"
env.gunicorn_port = 9099
env.clone_url = "git@github.com:yaniv14/OpComm.git"
env.webuser = "oc"
env.bkuser = "ocbk"
env.code_dir = '/home/%s/OpenComm/' % env.user
env.log_dir = '%slogs/' % env.code_dir
env.venv_dir = '/home/%s/.virtualenvs/oc' % env.user
env.venv_command = '.  %s/bin/activate' % env.venv_dir
env.pidfile = '/home/%s/oc.pid' % env.webuser
env.backup_dir = '/home/%s/backups/db/' % env.user
env.vhost = '139.162.215.52'


@task
def qa():
    env.instance = 'qa'
    env.hosts = [env.vhost]
    env.port = 9022
    env.redirect_host = None


@task
def ocean():
    env.instance = 'oc'
    env.hosts = [env.vhost]
    env.ocean = True
    env.redirect_host = 'www.%s' % env.vhost


@task
def initial_project_setup():
    create_webuser_and_db()
    clone_project()
    create_venv()
    project_setup()


@task
def project_setup():
    project_mkdirs()
    create_local_settings()
    deploy(restart=False)
    celery_setup()
    gunicorn_setup()
    supervisor_setup()
    nginx_setup()


try:
    from local_fabfile import *
except ImportError:
    pass
