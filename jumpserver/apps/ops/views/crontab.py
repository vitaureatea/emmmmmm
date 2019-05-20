from django.shortcuts import render, redirect
from django.http import JsonResponse
import simplejson, random, os, difflib
from django.contrib.auth.decorators import login_required
from django.conf import settings

from assets.models import SystemUser, Asset
from ..models import CrontabTask, GetCrontab
from ..crontab.task_crontab import crontab_task, update_host_crontab, get_iis_site
from audits.models import CrontabLog


@login_required(login_url='/users/login/')
def crontabcreateview(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            from perms.utils import AssetPermissionUtil
            user = request.user
            util = AssetPermissionUtil(user)
            system_users = [s for s in util.get_system_users()]
            type = 'lin'
            return render(request, 'ops/crontab_create_task.html', {'system_users': system_users, 'type': type})
        if request.method == 'POST':
            payload = simplejson.loads(request.body)
            host_id = payload['host_id']
            run_as = payload['run_as']
            run_as = SystemUser.objects.get(pk=run_as)
            payload = payload['t_data']

            file_dir = settings.PROJECT_DIR + "/data/crontab_scripts/"
            full_path = file_dir + ''.join([random.choice('1324345656789ewretrytuyusfdgfh') for i in range(20)]) + '.sh'

            with open(full_path, 'w') as file:
                file.write(payload['config'].strip())
            os.system('dos2unix %s' % full_path)

            log = CrontabLog()
            log.user = request.user.username
            # log.system_user = run_as.name + '(%s)' % run_as.username
            log.operate = '创建Crontab'
            log.remote_addr = request.META['HTTP_X_FORWARDED_FOR']
            log.filename = '创建：'
            log.hosts_name(host_id)
            log.save()

            task_id = []
            for id in host_id:
                crontab = CrontabTask()
                crontab.name = payload['name'].strip()
                crontab.run_as = run_as
                # crontab.comment = payload['comment'].strip()
                crontab.scripts_path = full_path
                if len(payload['time_minute'].strip()) == 0:
                    crontab.crontab_minute = '*'
                else:
                    crontab.crontab_minute = payload['time_minute'].strip()
                if len(payload['time_hour'].strip()) == 0:
                    crontab.crontab_hour = '*'
                else:
                    crontab.crontab_hour = payload['time_hour'].strip()
                if len(payload['time_day']) == 0:
                    crontab.crontab_day = '*'
                else:
                    crontab.crontab_day = payload['time_day'].strip()
                if len(payload['time_month'].strip()) == 0:
                    crontab.crontab_month = '*'
                else:
                    crontab.crontab_month = payload['time_month'].strip()
                if len(payload['time_week'].strip()) == 0:
                    crontab.crontab_week = '*'
                else:
                    crontab.crontab_week = payload['time_week'].strip()
                crontab.status = 1
                crontab.save()
                host_id = Asset.objects.get(pk=id)
                crontab.hosts.add(host_id)

                crontab_obj = CrontabTask.objects.get(pk=crontab.id)
                hosts = crontab_obj.hosts.all()
                # add_daily_task(crontab.id, run_as, hosts)
                crontab_task.delay(crontab_obj, run_as, hosts, log, hosts[0])
                task_id.append(crontab.id)
            return JsonResponse({
                'status': '1',
                'task_id': task_id
            })
    else:
        return redirect('/')


@login_required(login_url='/users/login/')
def getstatus(request):
    status = []
    for task_id in request.GET.getlist('task_id[]'):
        dic = {}
        obj = CrontabTask.objects.get(pk=task_id)
        # dic['host_name'] = list(obj.hosts.all().values('hostname'))
        # dic['message'] = obj.site_message
        dic['status'] = obj.status
        status.append(dic)
    return JsonResponse({
        'status': status
    })


@login_required(login_url='/users/login/')
def crontablistview(request):
    from perms.utils import AssetPermissionUtil
    user = request.user
    util = AssetPermissionUtil(user)
    assets = [s for s in util.get_assets()]
    query_list = []
    for asset in assets:
        if asset.platform == 'Linux':
            obj = GetCrontab.objects.filter(hosts__id=asset.id)
            for obj in obj:
                dic = {}
                dic['hostid'] = asset.id
                dic['hostip'] = asset.ip
                dic['hostname'] = asset.hostname
                try:
                    try:
                        dic['message'] = eval(obj.message)[asset.hostname]['stdout']
                    except Exception as e:
                        dic['message'] = eval(obj.message)[asset.hostname]['err']
                except Exception as e:
                    pass
                try:
                    dic_ = [s for s in query_list][0]
                    if asset.ip == dic_['hostip']:
                        pass
                    else:
                        query_list.append(dic)
                except Exception as e:
                    query_list.append(dic)
    return render(request, 'ops/crontab_view_list.html', {'crontab_list': query_list})


@login_required(login_url='/users/login/')
def crontabupdate(request, host_id):
    if request.user.is_superuser:
        message = ''
        if request.method == 'POST':
            obj = GetCrontab.objects.get(hosts=host_id)
            host_obj = obj.hosts.all()[0]
            log = CrontabLog()
            log.user = request.user.username
            log.operate = '变动'
            log.remote_addr = request.META['HTTP_X_FORWARDED_FOR']
            # d = difflib.Differ()
            # remove = ''.join(list(d.compare(eval(obj.message)[host_obj.hostname]['stdout'].splitlines(),
            #                         request.POST['config'].replace('\r', '').strip().splitlines())))
            try:
                x = eval(obj.message)[host_obj.hostname]['stdout']
                y = request.POST['config'].replace('\r', '').strip()
                opcodes = difflib.SequenceMatcher(None, x, y).get_opcodes()
                for op, af, at, bf, bt in opcodes:
                    if op != 'equal':
                        log.filename = op, x[af:at], y[bf:bt]
            except Exception as e:
                pass
            log.hosts_name(host_id)

            result = update_host_crontab(host_id, request.POST['config'].replace('\r', '').strip())
            if result:
                message = result
                log.is_success = False
                log.save()
            else:
                message = ''
                log.is_success = True
                get_crontab = GetCrontab.objects.get(hosts=host_id)
                try:
                    message = eval(get_crontab.message)
                    message[host_obj.hostname]['stdout'] = request.POST['config'].replace('\r', '').strip()
                except Exception as e:
                    pass
                get_crontab.message = message
                get_crontab.save()
                log.save()
                return redirect('/ops/crontab/view/')

        obj = GetCrontab.objects.get(hosts=host_id)
        host_obj = obj.hosts.all()[0]
        lables = {}
        try:
            lables['crontab'] = eval(obj.message)[host_obj.hostname]['stdout']
        except Exception as e:
            lables['crontab'] = ''
        lables['hostid'] = host_id
        lables['hostip'] = host_obj.ip
        lables['hostname'] = host_obj.hostname
        return render(request, 'ops/crontab_update_task.html', {'lable': lables, 'message': message})
    else:
        return redirect('/')


@login_required(login_url='/users/login/')
def removecrontabtask(request):

    return JsonResponse({
        'status': '1'
    })