import datetime
import os.path

from fabric import operations
from fabric.api import *
from fabric.contrib.console import confirm


def do_sleep(sleep_time):
    import time
    sleep_time = int(sleep_time)
    print('Going to sleep for {} seconds'.format(sleep_time))
    time.sleep(sleep_time)
    print('After sleeping')


def do_load_db_from_file(filename):
    drop_command = "drop schema public cascade; create schema public;"
    local('''python -c "print '{}'" | python manage.py dbshell'''.format(
        drop_command, filename))

    cmd = "gunzip -c" if filename.endswith('.gz') else "cat"
    local('{} {} | python manage.py dbshell'.format(cmd, filename))


@task
def load_db_from_file(filename, sleep_time=None):
    if not os.path.isfile(filename):
        abort("Unknown file {}".format(filename))

    if not confirm(
            "DELETE local db and load from backup file {}?".format(filename)):
        abort("Aborted.")
    if sleep_time:
        do_sleep(sleep_time)
    do_load_db_from_file(filename)


@task
def remote_backup_and_load(sleep_time=None):
    from . import db
    if not confirm(
            "Do remote backup and DELETE local db and load from remote {}?"):
        abort("Aborted.")
    if sleep_time:
        do_sleep(sleep_time)
    filename = db.remote_backup_db()
    do_load_db_from_file(filename)


@task
def remote_backup():
    from . import db
    filename = db.remote_backup_db()
    print(filename)


@task
def load_db_from_latest(sleep_time=None):
    if not confirm(
            "Are you sure you want to download latest sql.gz and replace database?"):
        abort("Aborted")
    if sleep_time:
        do_sleep(sleep_time)
    filenames = operations.get("/home/oc/backups/db/latest.sql.gz",
                               "{}/{}/latest.sql.gz".format(env.host,
                                                            datetime.datetime.now().strftime(
                                                                "%Y_%m_%d_%H_%M_%S")
                                                            ))
    filename = list(filenames)[0]
    do_load_db_from_file(filename)


@task
def create_db_user():
    local("sudo -u postgres createuser -s oc -P")  # password = "webtimi"


@task
def create_db():
    local("sudo -u postgres createdb -O oc oc")


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
    with lcd(base_dir):
        local("tar czf uploads.tar.gz uploads")
        local("rm -rf uploads")
    return fullpath


@task
def fetch_uploads(folder=''):
    """Fetch uploads folder from target server."""
    cmd = 'rsync -aP {server}:/home/oc/OpComm/uploads/{folder} uploads/{folder}'.format(
        server="{}@{}".format(env.user, env.vhost),
        folder=folder,
    )
    print(cmd)
    # local(cmd)
