from collections import namedtuple
import json, time

from .inventory import JMSInventory
from .ansible.runner import CommandRunner
from .celery import app
from audits.models import UpFileLog, IISLog


Options = namedtuple('Options', [
        'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
        'module_path', 'forks', 'remote_user', 'private_key_file', 'timeout',
        'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
        'scp_extra_args', 'become', 'become_method', 'become_user',
        'verbosity', 'check', 'extra_vars', 'playbook_path', 'passwords',
        'diff', 'gathering', 'remote_tmp',
    ])


class FileFile(object):

    def __init__(self, hosts, file_cmd, run_as):
        self.hosts = hosts
        self.run_as = run_as
        self.command = file_cmd

    @property
    def inventory(self):
        return JMSInventory(self.hosts, run_as=self.run_as)

    @property
    def module(self):
        obj = self.hosts
        for item in obj:
            if item.platform == 'Windows' or item.platform == 'Windows2016':
                return 'win_copy'
            else:
                return 'copy'

    @property
    def set_options(self):
        obj = self.hosts
        for item in obj:
            if item.platform == 'Windows' or item.platform == 'Windows2016':
                options = Options(
                    listtags=False,
                    listtasks=False,
                    listhosts=False,
                    syntax=False,
                    timeout=30,
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
            else:
                options = Options(
                    listtags=False,
                    listtasks=False,
                    listhosts=False,
                    syntax=False,
                    timeout=30,
                    connection='ssh',
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

    @property
    def result(self):
        if self._result:
            return json.loads(self._result)
        else:
            return {}

    @result.setter
    def result(self, item):
        self._result = json.dumps(item)

    def run(self):
        runner = CommandRunner(self.inventory, self.set_options)
        try:
            result = runner.execute(self.command, 'all', self.module, )
            self.result = result.results_command
        except Exception as e:
            self.result = {"error": str(e)}

        return self.result



class IisRestart(FileFile):
    def __init__(self, hosts, iis_cmd, run_as):
        super().__init__(hosts, iis_cmd, run_as)

    @property
    def module(self):
        obj = self.hosts
        for item in obj:
            if item.platform == 'Windows' or item.platform == 'Windows2016':
                return 'win_iis_website'
            else:
                return False



class IisCreate(IisRestart):
    def __init__(self, hosts, iis_cmd, run_as):
        super().__init__(hosts, iis_cmd, run_as)


class PoolCreate(FileFile):
    def __init__(self, hosts, iis_cmd, run_as):
        super().__init__(hosts, iis_cmd, run_as)

    @property
    def module(self):
        obj = self.hosts
        for item in obj:
            if item.platform == 'Windows' or item.platform == 'Windows2016':
                return 'win_iis_webapppool'
            else:
                return False


class IisBind(FileFile):
    def __init__(self, hosts, iis_cmd, run_as):
        super().__init__(hosts, iis_cmd, run_as)

    @property
    def module(self):
        obj = self.hosts
        for item in obj:
            if item.platform == 'Windows' or item.platform == 'Windows2016':
                return 'win_iis_webbinding'
            else:
                return False


class CrontabTasks(FileFile):
    def __init__(self, hosts, scripts, run_as):
        super().__init__(hosts, scripts, run_as)

    @property
    def module(self):
        return 'script'

class LinCmd(FileFile):
    def __init__(self, hosts, scripts, run_as):
        super().__init__(hosts, scripts, run_as)

    @property
    def module(self):
        return 'shell'


@app.task()
def startfile(file_obj, hosts, run_as, log_id):

    obj = file_obj
    obj.message = '分发中'
    obj.save()
    file_cmd = 'src=%s dest=%s' % (file_obj.local_file_path, file_obj.remove_file_path)
    task_obj = FileFile(hosts, file_cmd, run_as)
    result = task_obj.run()
    obj = file_obj
    obj.message = result
    obj.status = 2
    obj.save()
    log = UpFileLog.objects.get(pk=log_id)
    i = str(result).find('Error')
    if i != -1:
        log.is_success = False
    else:
        log.is_success = True
    log.save()
    return True


@app.task()
def restartiis(iis_obj, hosts, run_as, log_id):

    try:
        site_list = iis_obj.site.split(',')
    except Exception as e:
        site_list = iis_obj.site.split()

    result_ = []
    for site in site_list:
        if site.strip() == '':
            continue
        else:
            iis_cmd = 'name=%s state=restarted' % site.strip()
            task_obj = IisRestart(hosts, iis_cmd, run_as)
            result = task_obj.run()
            result['site'] = site
            result_.append(result)

    iis_obj.message = result_
    iis_obj.status = 2
    iis_obj.save()
    log = IISLog.objects.get(pk=log_id)
    i = str(result).find('Error')
    if i != -1:
        log.is_success = False
    else:
        log.is_success = True
    log.save()
    return True


def createpool(iis_obj, hosts, run_as):

    if len(iis_obj.pool.strip()) == 0:
        pool_name = iis_obj.site.strip()
        iis_cmd = 'name=%s state=started' % iis_obj.site.strip()
    else:
        pool_name = iis_obj.pool.strip()
        iis_cmd = 'name=%s state=started' % iis_obj.pool.strip()

    task_obj = PoolCreate(hosts, iis_cmd, run_as)
    result = task_obj.run()

    # iis_obj.pool_message = result
    # iis_obj.save()
    pool_result = [result, pool_name]

    return pool_result


def iisbind(iis_obj, hosts, run_as, result_, log_id):

    try:
       dom_list = iis_obj.dom.split(',')
    except Exception as e:
       dom_list = iis_obj.dom.split('')

    iis_cmd = 'name=%s state=absent ' % iis_obj.site
    task_obj = IisBind(hosts, iis_cmd, run_as)
    task_obj.run()

    cont = 0
    for dom in dom_list:
        if dom.strip() == '':
            cont += 1
            continue
        else:
            iis_cmd = 'name=%s state=present host_header=%s' % (iis_obj.site, dom)
            task_obj = IisBind(hosts, iis_cmd, run_as)
            task_obj.run()

            iis_cmd = 'name=%s state=restarted' % iis_obj.site
            task_obj = IisRestart(hosts, iis_cmd, run_as)
            result = task_obj.run()

            iis_obj.site_message = result
            iis_obj.status = 2
            iis_obj.save()
            log = IISLog.objects.get(pk=log_id)
            i = str(result).find('Error')
            if i != -1:
                log.is_success = False
            else:
                log.is_success = True
            log.save()

    if len(dom_list) == cont:
        iis_obj.site_message = result_
        iis_obj.status = 2
        iis_obj.save()
        log = IISLog.objects.get(pk=log_id)
        i = str(result).find('Error')
        if i != -1:
            log.is_success = False
        else:
            log.is_success = True
        log.save()
    return True


@app.task()
def createiis(iis_obj, hosts, run_as, log_id):
    pool_result = createpool(iis_obj, hosts, run_as)
    result = pool_result[0]
    for key, vaule in result.items():
        if 'Connection refused' in str(vaule):
            iis_obj.site_message = result
            iis_obj.status = 2
            iis_obj.save()
            return True

    pool_name = pool_result[1]
    if len(iis_obj.dom.strip()) != 0:
        if iis_obj.port:
            iis_cmd = 'name=%s state=started application_pool=%s physical_path=%s port=%s' % (iis_obj.site, pool_name, iis_obj.pdir, iis_obj.port)
        else:
            iis_cmd = 'name=%s state=started application_pool=%s physical_path=%s' % (iis_obj.site, pool_name, iis_obj.pdir)
        task_obj = IisCreate(hosts, iis_cmd, run_as)
        result_ = task_obj.run()
        iisbind(iis_obj, hosts, run_as, result_, log_id)
    if len(iis_obj.dom.strip()) == 0:
        if iis_obj.port:
            iis_cmd = 'name=%s state=started application_pool=%s physical_path=%s port=%s' % (iis_obj.site, pool_name, iis_obj.pdir, iis_obj.port)
        else:
            iis_cmd = 'name=%s state=started application_pool=%s physical_path=%s' % (iis_obj.site, pool_name, iis_obj.pdir)
        #iis_cmd = 'name=%s state=started application_pool=%s physical_path=%s' % (iis_obj.site, pool_name, iis_obj.pdir)
        task_obj = IisCreate(hosts, iis_cmd, run_as)
        result = task_obj.run()
        iis_obj.site_message = result
        iis_obj.status = 2
        iis_obj.save()
        from .crontab.task_crontab import get_iis_site
        get_iis_site()
        log = IISLog.objects.get(pk=log_id)
        i = str(result).find('Error')
        if i != -1:
            log.is_success = False
        else:
            log.is_success = True
        log.save()
    return True