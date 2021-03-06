from fab_tools.server import *
from fab_tools.project import *
from fab_tools.dev import *

PROJ_DIR = os.path.abspath(os.path.dirname(__file__))
CONF_DIR = os.path.abspath(os.path.join(PROJ_DIR, 'conf'))

env.project = "oc"
env.vhost = '139.162.215.52'
env.hosts = [env.vhost]
env.port = 22
env.redirect_host = 'www.%s' % env.vhost
env.user = "oc"
env.gunicorn_port = 9099
env.clone_url = "git@github.com:yaniv14/OpComm.git"
env.webuser = "oc"
env.bkuser = "ocbk"
env.code_dir = '/home/%s/OpenComm/' % env.user
env.log_dir = '%slog/' % env.code_dir
env.venv_dir = '/home/%s/.virtualenvs/oc' % env.user
env.venv_command = '. %s/bin/activate' % env.venv_dir
env.pidfile = '/home/%s/oc.pid' % env.webuser
env.backup_dir = '/home/%s/backups/db/' % env.bkuser


@task
def qa():
    env.instance = 'qa'
    env.hosts = [env.vhost]
    env.webuser = "oc_qa"
    env.pidfile = '/home/%s/oc_qa.pid' % env.webuser
    env.port = 9022
    env.redirect_host = None


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
    from .local_fabfile import *
except ImportError:
    pass
