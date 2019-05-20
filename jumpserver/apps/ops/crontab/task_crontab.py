from apscheduler.triggers.cron import CronTrigger
from celery import shared_task
import paramiko, json
from django.db.models import Q

from collections import namedtuple
from . import scheduler
from ..models import CrontabTask, GetCrontab, GetIISSite
from ..an_que import LinCmd, FileFile
from ..celery import app
from assets.models import SystemUser, Asset
from ..celery.decorator import (
    register_as_period_task, after_app_shutdown_clean_periodic,
    after_app_ready_start
)
from ..ansible import AdHocRunner, AnsibleError
from ..inventory import JMSInventory


@app.task()
def crontab_task(crontab_obj, run_as, hosts, log, hostobj):
    mk_cmd = 'mkdir -p /usr/src/contab_scripts/'
    task_obj = LinCmd(hosts, mk_cmd, run_as)
    result = task_obj.run()
    i = str(result).find('Error')
    if i != -1:
        log.is_success = False
    else:
        log.is_success = True
    file_cmd = 'src=%s dest=/usr/src/contab_scripts/' % crontab_obj.scripts_path
    task_obj = FileFile(hosts, file_cmd, run_as)
    result = task_obj.run()
    i = str(result).find('Error')
    if i != -1:
        log.is_success = False
    else:
        log.is_success = True
    file_name = crontab_obj.scripts_path.split('/')[-1]
    crontab_cmd = 'echo -e "#%s\n%s %s %s %s %s /bin/bash /usr/src/contab_scripts/%s" >> /var/spool/cron/root ' % (
                                                                     crontab_obj.name,
                                                                     crontab_obj.crontab_minute,
                                                                     crontab_obj.crontab_hour,
                                                                     crontab_obj.crontab_day,
                                                                     crontab_obj.crontab_month,
                                                                     crontab_obj.crontab_week,
                                                                     file_name,)
    task_obj = LinCmd(hosts, crontab_cmd, run_as)
    result = task_obj.run()
    crontab_obj.crontab_log = result
    crontab_obj.status = 2
    crontab_obj.save()
    i = str(result).find('Error')
    if i != -1:
        log.is_success = False
    else:
        log.is_success = True
        get_crontab = GetCrontab.objects.get(hosts=hostobj.id)
        try:
            message = eval(get_crontab.message)
            message[hostobj.hostname]['stdout'] = message[hostobj.hostname]['stdout'] + " #%s \n %s %s %s %s %s /bin/bash /usr/src/contab_scripts/%s" % (
                                                                     crontab_obj.name,
                                                                     crontab_obj.crontab_minute,
                                                                     crontab_obj.crontab_hour,
                                                                     crontab_obj.crontab_day,
                                                                     crontab_obj.crontab_month,
                                                                     crontab_obj.crontab_week,
                                                                     file_name,)
            get_crontab.message = message
        except Exception as e:
            pass
        try:
            log.filename = log.filename + " #%s \n %s %s %s %s %s /bin/bash /usr/src/contab_scripts/%s" % (
                crontab_obj.name,
                crontab_obj.crontab_minute,
                crontab_obj.crontab_hour,
                crontab_obj.crontab_day,
                crontab_obj.crontab_month,
                crontab_obj.crontab_week,
                file_name,)
        except Exception as e:
            pass
        get_crontab.save()
    log.save()


@shared_task
@register_as_period_task(interval=900)
def get_host_crontab():
    assets = Asset.objects.filter(platform='Linux')
    for asset in assets:
        auth = asset.get_auth_info()
        i = GetCrontab.objects.filter(hosts__id=asset.id)
        if i:
            get_crontab = GetCrontab.objects.get(hosts=asset.id)
            try:
                t = paramiko.SSHClient()
                t.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                if auth.get('password') is not None:
                    username = auth['username']
                    password = auth['password']
                    t.connect(asset.ip, asset.port, username, password)
                else:
                    username = auth['username']
                    private_key = paramiko.RSAKey.from_private_key_file(auth['private_key'])
                    t.connect(asset.ip, asset.port, username, private_key, timeout=10)
                stdin, stdout, stderr = t.exec_command('crontab -l')
                stderr = stderr.read().decode()
                stdout = stdout.read().decode()
                message = json.dumps({asset.hostname: {'stderr': stderr, 'stdout': stdout}})
            except Exception as e:
                message = json.dumps({asset.hostname: {'err': {'ERROR': '主机连接不通'}}})
            # get_crontab.hosts.clear()
            get_crontab.message = message
            get_crontab.save()
            # get_crontab.hosts.add(asset)
            t.close()
        else:
            get_crontab = GetCrontab()
            get_crontab.save()
            get_crontab.hosts.add(asset)
            try:
                t = paramiko.SSHClient()
                t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                username = auth['username']
                if auth.get('password') is not None:
                    password = auth['password']
                    t.connect(asset.ip, asset.port, username, password)
                else:
                    # username = auth['username']
                    private_key = paramiko.RSAKey.from_private_key_file(auth['private_key'])
                    t.connect(asset.ip, asset.port, username, private_key)
                stdin, stdout, stderr = t.exec_command('crontab -l')
                stderr = stderr.read().decode()
                stdout = stdout.read().decode()
                message = json.dumps({asset.hostname: {'stderr': stderr, 'stdout': stdout}})
            except Exception as e:
                message = json.dumps({asset.hostname: {'err': {'ERROR': '主机连接不通'}}})
            if GetCrontab.objects.filter(hosts__id=asset.id):
                t.close()
            else:
                get_crontab.message = message
                get_crontab.save()
                t.close()


def update_host_crontab(host_id, crontab):
    asset = Asset.objects.get(id=host_id)
    auth = asset.get_auth_info()
    t = paramiko.SSHClient()
    t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if auth.get('password') is not None:
            username = auth['username']
            password = auth['password']
            t.connect(asset.ip, asset.port, username, password)
            stdin, stdout, stderr = t.exec_command('echo -e "%s" >  /var/spool/cron/root' % crontab)
            stderr = stderr.read().decode()
            stdout = stdout.read().decode()
            t.close()
        else:
            username = auth['username']
            private_key = paramiko.RSAKey.from_private_key_file(auth['private_key'])
            t.connect(asset.ip, asset.port, username, private_key)
            stdin, stdout, stderr = t.exec_command('echo -e "%s" >  /var/spool/cron/root' % crontab)
            stderr = stderr.read().decode()
            stdout = stdout.read().decode()
            t.close()
    except Exception as e:
        return e


Options = namedtuple('Options', [
        'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
        'module_path', 'forks', 'remote_user', 'private_key_file', 'timeout',
        'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
        'scp_extra_args', 'become', 'become_method', 'become_user',
        'verbosity', 'check', 'extra_vars', 'playbook_path', 'passwords',
        'diff', 'gathering', 'remote_tmp',
    ])


def options():
    options = Options(
        listtags=False,
        listtasks=False,
        listhosts=False,
        syntax=False,
        timeout=10,
        connection='winrm',
        module_path='',
        forks=10,
        remote_user='root',
        private_key_file=None,
        ssh_common_args="",
        ssh_extra_args="",
        sftp_extra_args="",
        scp_extra_args="",
        become=None,
        become_method=None,
        become_user=None,
        verbosity=None,
        extra_vars=[],
        check=False,
        playbook_path='/etc/ansible/',
        passwords=None,
        diff=False,
        gathering='implicit',
        remote_tmp='/tmp/.ansible'
    )
    return options


@shared_task
@register_as_period_task(interval=900)
def get_iis_site():
    assets = Asset.objects.filter(Q(platform='Windows') | Q(platform='Windows2016'))
    for asset in assets:
        if GetIISSite.objects.filter(hosts__id=asset.id):
            site = GetIISSite.objects.get(hosts=asset.id)
            inventory = JMSInventory(assets=site.hosts.all(), run_as_admin=True)
            runner = AdHocRunner(inventory, options=options())
            result = runner.run(
                [{"name": "get_iis_site",
                  "action": {"module": "win_shell", 'args': '\\Windows\\System32\\inetsrv\\appcmd.exe list sites'}}],
                'all',
                'get_iis_site',
            )
            site.message = result.results_command
            site.save()
        else:
            iissit = GetIISSite()
            iissit.save()
            iissit.hosts.add(asset)
            inventory = JMSInventory(assets=iissit.hosts.all(), run_as_admin=True)
            runner = AdHocRunner(inventory, options=options())
            result = runner.run(
                [{"name": "get_iis_site",
                  "action": {"module": "win_shell", 'args': '\\Windows\\System32\\inetsrv\\appcmd.exe list sites'}}],
                'all',
                'get_iis_site',
            )
            iissit.message = result.results_command
            iissit.save()


@app.task()
def Manual_get_iis_site():
    get_iis_site()

def add_daily_task(task_id, run_as, hosts):

    crontab = CrontabTask.objects.get(pk=task_id)
    scheduler.add_job(func=crontab_task,
                      args=[task_id, run_as, hosts],
                      trigger=CronTrigger.from_crontab('%s %s %s %s %s' % (crontab.crontab_month,
                                                                           crontab.crontab_day,
                                                                           crontab.crontab_week,
                                                                           crontab.crontab_hour,
                                                                           crontab.crontab_minute)),
                      id=str(crontab.id),
                      jobstore='eazyops',
                      replace_existing=True)

    return True