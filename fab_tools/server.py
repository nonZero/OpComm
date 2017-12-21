from __future__ import unicode_literals

import datetime

from fabric.api import *
from fabric.contrib.files import upload_template, uncomment, append, comment
from fabtools import cron
from six import StringIO

APT_PACKAGES = [
    'unattended-upgrades',
    'ntp',
    'postgresql',
    'postgresql-contrib',
    'nginx',
    'supervisor',
    'virtualenvwrapper',
    'git',
    'python-dev',
    'libpq-dev',
    'libjpeg-dev',
    'libjpeg8',
    'zlib1g-dev',
    'libfreetype6',
    'libfreetype6-dev',
    'postfix',
    'fail2ban',
    'redis-server',
    'htop',
    'rabbitmq-server',
]

AUTO_RENEW_SCRIPT = '/home/certbot/auto-renew.sh'


@task
def disable_ipv6():
    append('/etc/sysctl.conf', [
        'net.ipv6.conf.all.disable_ipv6 = 1',
        'net.ipv6.conf.default.disable_ipv6 = 1',
        'net.ipv6.conf.lo.disable_ipv6 = 1',
    ], use_sudo=True)
    run('sudo sysctl -p')


@task
def update_server_pkgs():
    run("sudo apt-get -qq update", pty=False)
    run("sudo apt-get -q upgrade -y", pty=False)


@task
def install_server_pkgs():
    update_server_pkgs()
    pkgs = APT_PACKAGES
    run("sudo apt-get -q install -y %s" % " ".join(pkgs), pty=False)


@task
def server_setup():
    disable_ipv6()
    install_server_pkgs()


@task
def host_type():
    run('uname -s')


@task
def hard_reload():
    run("sudo supervisorctl restart %s" % env.webuser)


@task
def very_hard_reload():
    run("sudo service supervisor stop")
    run("sudo service supervisor start")


@task
def log(n=50):
    run("tail -n{} {}*".format(n, env.log_dir))


@task
def nginx_log(n=50):
    run("tail -n{} /var/log/nginx/error.log".format(n))


@task
def create_webuser_and_db():
    run("sudo adduser %s --gecos '' --disabled-password" % env.webuser)
    run("sudo -iu postgres createuser %s -S -D -R" % env.webuser)
    run("sudo -iu postgres createdb %s -O %s" % (env.webuser, env.webuser))
    run("sudo -iu postgres psql -c \"alter user %s with password '%s';\"" % (
        env.webuser, env.webuser))


@task
def create_backup_user():
    run("sudo adduser %s --gecos '' --disabled-password" % env.bkuser)


@task
def nginx_relog(reload=True):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    sudo('cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.{ts}'.format(ts=ts))
    comment('/etc/nginx/nginx.conf',
            '^\s*[^#]\s*access_log /var/log/nginx/access.log', use_sudo=True)
    # comment('/etc/nginx/nginx.conf','\s*[^#]\s*error_log /var/log/nginx/error.log',use_sudo=True)
    put('conf/nginx.logs.conf', '/etc/nginx/conf.d/nginx.logs.conf',
        use_sudo=True)
    if reload:
        sudo('nginx -t')
        sudo('service nginx start')
        sudo('service nginx reload')


@task
def nginx_setup(secure=False):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    uncomment('/etc/nginx/nginx.conf',
              'server_names_hash_bucket_size\s+64',
              use_sudo=True)

    nginx_conf1 = '/etc/nginx/sites-available/%s.conf' % env.webuser

    src = 'conf/nginx.secure.conf.template'

    sudo('cp {f} {f}.{ts}'.format(f=nginx_conf1, ts=ts))

    upload_template(
        src, nginx_conf1,
        {
            'host': env.vhost,
            'redirect_host': env.redirect_host,
            'dir': env.code_dir,
            'port': env.gunicorn_port,
            'secure': secure,
        },
        use_sudo=True,
        use_jinja=True,
    )

    run('sudo rm -f /etc/nginx/sites-enabled/default')

    nginx_conf2 = '/etc/nginx/sites-enabled/%s.conf' % env.webuser
    run('sudo ln -fs %s %s' % (nginx_conf1, nginx_conf2))

    nginx_relog(reload=False)

    run('sudo nginx -t')
    run('sudo service nginx start')
    run('sudo service nginx reload')


@task
def gen_prod_nginx_in_tmp():
    nginx_conf1 = '/tmp/%s.conf' % env.webuser

    src = 'conf/nginx.secure.conf.template'

    upload_template(
        src, nginx_conf1,
        {
            'host': env.vhost,
            'redirect_host': env.redirect_host,
            'dir': env.code_dir,
            'port': env.gunicorn_port,
            'secure': True,
        },
        use_sudo=True,
        use_jinja=True,
    )


@task
def celery_setup():
    create_worker()


def create_worker(name="worker.sh", extra=""):
    with cd(env.code_dir):
        upload_template('conf/worker.sh.template',
                        env.code_dir + name,
                        {
                            'venv': env.venv_dir,
                            'extra': extra,
                        }, mode=0o777, use_jinja=True)


@task
def gunicorn_setup():
    with cd(env.code_dir):
        upload_template('conf/server.sh.template',
                        env.code_dir + 'server.sh',
                        {
                            'venv': env.venv_dir,
                            'port': env.gunicorn_port,
                            'pidfile': env.pidfile,
                        }, mode=0o777, use_jinja=True)


@task
def supervisor_reread():
    run("sudo supervisorctl reread")
    run("sudo supervisorctl update")


@task
def supervisor_setup():
    with cd(env.code_dir):
        upload_template('conf/supervisor.conf.template',
                        env.code_dir + 'conf/supervisor.conf',
                        {
                            'dir': env.code_dir,
                            'webuser': env.webuser,
                            'logdir': env.log_dir,
                        }, mode=0o777, use_jinja=True)

        run(
            'sudo ln -fs %sconf/supervisor.conf /etc/supervisor/conf.d/%s.conf'
            % (env.code_dir, env.webuser))
    supervisor_reread()


@task
def project_mkdirs():
    """Creates empty directories for logs, uploads and search indexes"""
    with cd(env.code_dir):
        run('mkdir -pv %s' % env.log_dir)

        dirs = ['uploads', 'web-logs']
        for dirname in dirs:
            run('mkdir -pv {}'.format(dirname))
            run('sudo chown -v {} {}'.format(env.webuser, dirname))


@task
def status():
    run("sudo supervisorctl status")


@task
def update_time():
    run("sudo ntpdate ntp.ubuntu.com")


@task
def install_certbot():
    # FIRST use nginx_setup (unsecure)
    # THEN run this
    # THEN nginx_setup:secure=1
    #
    # For "Cannot add PPA. Please check that the PPA name or format is correct" error, use:
    # sudo("apt-get install -q --reinstall ca-certificates")
    # Source: https://askubuntu.com/questions/429803/cannot-add-ppa-please-check-that-the-ppa-name-or-format-is-correct

    sudo("add-apt-repository ppa:certbot/certbot")
    sudo("apt-get -qq update", pty=False)
    sudo("apt-get install -q -y certbot", pty=False)

    sudo("adduser certbot --gecos '' --disabled-password")
    upload_template('conf/certbot.ini.template', '/home/certbot/certbot.ini', {
        'host': env.vhost,
    }, use_sudo=True, use_jinja=True, )
    create_certbot_renew_script()
    for s in ['webroot', 'conf', 'work', 'logs']:
        sudo('mkdir -p /home/certbot/{}/'.format(s), user='certbot')
    renew_cert()
    backup_cert()


@task
def create_certbot_renew_script():
    put(StringIO(
        """#!/bin/bash\ncertbot certonly -c certbot.ini"""),
        AUTO_RENEW_SCRIPT,
        use_sudo=True, mode=0o775)


@task
def backup_cert():
    get("/home/certbot/conf/", "%(host)s/certbot/%(path)s", use_sudo=True)


@task
def renew_cert():
    with cd("/home/certbot/"):
        sudo(AUTO_RENEW_SCRIPT, user='certbot')
    sudo("service nginx reload")


CERTBOT_CRON = """MAILTO=yanivmirel@gmail.com
0 0 1 FEB,APR,JUN,AUG,OCT,DEC * sudo -u certbot {} && service nginx reload
"""


@task
def setup_certbot_cron():
    # timespec = "0 0 1 FEB,APR,JUN,AUG,OCT,DEC *"
    timespec = "0 10 1 * *"
    cmd = "cd /home/certbot && sudo -u certbot {} && service nginx reload".format(
        AUTO_RENEW_SCRIPT)
    cron.add_task("renew_ssl", timespec, "root", cmd)


@task
def check_ssl():
    cmd = "echo | openssl s_client -connect {}:443 | openssl x509 -noout -dates"
    local(cmd.format("www.opencommittee.co.il"))
