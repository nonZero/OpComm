import datetime
import os.path

from fabric import operations
from fabric.api import *


def make_backup():
    now = datetime.datetime.now()
    filename = now.strftime(
        "{}-{}-%Y-%m-%d-%H-%M.sql.gz".format(env.project, env.instance))
    sudo('mkdir -p {}/manual'.format(env.backup_dir))
    fullpath = os.path.join(env.backup_dir, 'manual', filename)
    sudo('sudo -u postgres pg_dump {} | gzip > {}'.format(env.webuser,
                                                          fullpath))
    return fullpath


@task
def backup_local(base_dir):
    now = datetime.datetime.now()
    filename = now.strftime(
        "{}-{}-%Y-%m-%d-%H-%M.sql.gz".format(env.project, "localhost"))
    local("mkdir {}".format(base_dir))
    fullpath = os.path.join(base_dir, filename)
    local('sudo -u postgres pg_dump {} | gzip > {}'.format(env.webuser,
                                                           fullpath))
    local("cp -r uploads {}".format(base_dir))
    return fullpath


@task
def remote_backup_db():
    path = make_backup()
    paths = operations.get(path)
    run('ls -alh {}'.format(path))
    return list(paths)[0]


@task
def backup_db():
    operations.get(make_backup())


@task
def dumpdata(*args, **kwargs):
    prefix = kwargs.get('prefix')
    assert len(args) >= 1, "must specify one appmodel"
    if not prefix:
        assert len(args) == 1, "Must specify prefix if more than appmodel"
        prefix = args[0]
    from fab_tools.project import virtualenv
    ddir = '/home/{}/backups/datadumps'.format(env.user)
    run('mkdir -p {}'.format(ddir))
    appmodels = " ".join(args)
    if kwargs.get('pk'):
        pks_arg = "--pks {}".format(kwargs['pk'])
    else:
        pks_arg = ""
    with virtualenv(env.code_dir):
        now = datetime.datetime.now()
        outfile = os.path.join(ddir, now.strftime(
            "{}-%Y-%m-%d-%H-%M.json.gz".format(prefix)))
        run("python manage.py dumpdata --indent 4 {} {} | gzip -c > {}".format(appmodels, pks_arg, outfile))
    paths = operations.get(outfile)
    path = list(paths)[0]
    print("To restore: python manage.py loaddata {}".format(path))
