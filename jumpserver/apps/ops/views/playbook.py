from django.shortcuts import render, redirect
from django.http import JsonResponse
import time, simplejson
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings

from assets.models import SystemUser, Asset
from ..models import File, IisRestart, IisCreate
from ..an_que import startfile, restartiis, createiis
from audits.models import UpFileLog, IISLog
from ..models import GetIISSite
from ..crontab.task_crontab import Manual_get_iis_site


class multitask_file_transfer(TemplateView):
    template_name = 'ops/multitask_file_transfer.html'

    def get_user_system_users(self):
        from perms.utils import AssetPermissionUtil
        user = self.request.user
        util = AssetPermissionUtil(user)
        system_users = [s for s in util.get_system_users()]
        return system_users

    def get_context_data(self, **kwargs):
        system_users = self.get_user_system_users()
        context = {
            'app': 'Ops',
            'system_users': system_users
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


@login_required(login_url='/users/login/')
def upload_file(request):
    file_dir = settings.PROJECT_DIR + "/data/media/upfile/"
    if request.method == 'POST':
        upfile = request.FILES['crowd_file']
        uppath = request.POST['remote_path']
        host_id = request.POST['host_id']
        run_as = request.POST['run_as']
        run_as = SystemUser.objects.get(pk=run_as)

        file_name = upfile.name.replace(' ', '')
        full_path = file_dir + file_name

        with open(full_path, 'wb') as file:
            for chunk in upfile.chunks():
                file.write(chunk)

        log = UpFileLog()
        log.user = request.user.username
        log.system_user = run_as.name + '(%s)' % run_as.username
        log.operate = '上传'
        log.remote_addr = request.META['HTTP_X_FORWARDED_FOR']
        log.filename = uppath + ' => %s' % file_name
        log.hosts_name(host_id)
        log.save()

        task_id = []
        for id in host_id.split(','):
            obj = File()
            obj.local_file_path = full_path
            obj.remove_file_path = uppath
            obj.status = 1
            obj.run_as = run_as
            obj.save()
            host_id = Asset.objects.get(pk=id)
            obj.hosts.add(host_id)

            file_obj = File.objects.get(pk=obj.id)
            if file_obj.hosts.all():
                hosts = file_obj.hosts.all()
                startfile.delay(file_obj, hosts, run_as, log.id)
            else:
                time.sleep(2)
                hosts = file_obj.hosts.all()
                startfile.delay(file_obj, hosts, run_as, log.id)
            task_id.append(obj.id)

    return JsonResponse({
        'task_id': task_id,
    })


@login_required(login_url='/users/login/')
def get_upstatus(request):

    status = []
    for task_id in request.GET.getlist('task_id[]'):
        dic = {}
        obj = File.objects.get(pk=task_id)

        dic['host_name'] = list(obj.hosts.all().values('hostname'))
        dic['message'] = obj.message
        dic['status'] = obj.status
        status.append(dic)
    return JsonResponse({
        'status': status
    })


#playbook
@login_required(login_url='/users/login/')
def createjobtemplates(request):
    #if request.user.is_superuser:
        if request.method == 'POST':
            payload = simplejson.loads(request.body)
            host_id = payload['host_id']
            run_as = payload['run_as']
            run_as = SystemUser.objects.get(pk=run_as)

            if '，' in payload['t_data']['cmd']:
                return JsonResponse({
                    'douhao': 1
                })
            if '。' in payload['t_data']['cmd']:
                return JsonResponse({
                    'douhao': 1
                })

            log = IISLog()
            log.user = request.user.username
            log.system_user = run_as.name + '(%s)' % run_as.username
            log.operate = payload['t_data']['modules']
            log.remote_addr = request.META['HTTP_X_FORWARDED_FOR']
            log.filename = payload['t_data']['cmd']
            log.hosts_name(host_id)
            log.save()

            task_id = []
            if payload['t_data']['modules'] == 'iis重启站点':
                for id in host_id:
                    ir = IisRestart()
                    ir.run_as = run_as
                    ir.site = payload['t_data']['cmd']
                    ir.status = 1
                    ir.save()
                    host_id = Asset.objects.get(pk=id)
                    ir.hosts.add(host_id)

                    iis_obj = IisRestart.objects.get(pk=ir.id)
                    if iis_obj.hosts.all():
                        hosts = iis_obj.hosts.all()
                        restartiis.delay(iis_obj, hosts, run_as, log.id)

                    task_id.append(ir.id)

            try:
                site_list = payload['t_data']['cmd'].split(',')
            except Exception as e:
                site_list = payload['t_data']['cmd'].split()

            return JsonResponse({
                'task_id': task_id,
                'site_list': site_list
            })

        if request.method == 'GET':
            from perms.utils import AssetPermissionUtil
            user = request.user
            util = AssetPermissionUtil(user)
            system_users = [s for s in util.get_system_users()]
            type = 'win'
            return render(request, 'ops/create_job_templates.html', {'system_users': system_users, 'type': type})
    #else:
    #    return redirect('/')



@login_required(login_url='/users/login/')
def get_iisstatus(request):

    status = []
    for task_id in request.GET.getlist('task_id[]'):
        dic = {}
        obj = IisRestart.objects.get(pk=task_id)

        dic['host_name'] = list(obj.hosts.all().values('hostname'))
        #dic['message'] = obj.message
        try:
            dic['message'] = eval(obj.message)
        except Exception as e:
            dic['message'] = ''

        dic['status'] = obj.status
        status.append(dic)
    return JsonResponse({
        'status': status
    })



@login_required(login_url='/users/login/')
def createwebsite(request):
    #if request.user.is_superuser:
        if request.method == 'POST':
            payload = simplejson.loads(request.body)
            host_id = payload['host_id']
            run_as = payload['run_as']
            run_as = SystemUser.objects.get(pk=run_as)

            if '，' in payload['t_data']['cmd'] and '，' in payload['t_data']['dom'] and '，' in payload['t_data']['ip'] and '，' in payload['t_data']['pdir'] and '，' in payload['t_data']['pool'] and '，' in payload['t_data']['port']:
                return JsonResponse({
                    'douhao': 1
                })
            if '。' in payload['t_data']['cmd'] and '。' in payload['t_data']['dom'] and '。' in payload['t_data']['ip'] and '。' in payload['t_data']['pdir'] and '。' in payload['t_data']['pool'] and '。' in payload['t_data']['port']:
                return JsonResponse({
                    'douhao': 1
                })
            if ',' in payload['t_data']['cmd']:
                return JsonResponse({
                    'douhao': 2
                })

            log = IISLog()
            log.user = request.user.username
            log.system_user = run_as.name + '(%s)' % run_as.username
            log.operate = payload['t_data']['modules']
            log.remote_addr = request.META['HTTP_X_FORWARDED_FOR']
            log.filename = payload['t_data']['cmd']
            log.hosts_name(host_id)
            log.save()

            task_id = []
            if payload['t_data']['modules'] == 'iis创建站点':
                for id in host_id:
                    ir = IisCreate()
                    ir.run_as = run_as
                    ir.site = payload['t_data']['cmd']
                    ir.dom = payload['t_data']['dom']
                    ir.ip = payload['t_data']['ip']
                    ir.pdir = payload['t_data']['pdir'].replace('\\', '/')
                    ir.pool = payload['t_data']['pool']
                    ir.port = payload['t_data']['port']
                    ir.status = 1
                    ir.save()
                    host_id = Asset.objects.get(pk=id)
                    ir.hosts.add(host_id)

                    iis_obj = IisCreate.objects.get(pk=ir.id)
                    if iis_obj.hosts.all():
                        hosts = iis_obj.hosts.all()
                        createiis.delay(iis_obj, hosts, run_as, log.id)
                    task_id.append(ir.id)

            try:
                site_list = payload['t_data']['cmd'].split(',')
            except Exception as e:
                site_list = payload['t_data']['cmd'].split()

            return JsonResponse({
                'task_id': task_id,
                'site_list': site_list
            })

        else:
            return redirect('/')
    #else:
    #    return redirect('/')



@login_required(login_url='/users/login/')
def get_ciisstatus(request):

    status = []
    for task_id in request.GET.getlist('task_id[]'):
        dic = {}
        obj = IisCreate.objects.get(pk=task_id)

        dic['host_name'] = list(obj.hosts.all().values('hostname'))
        dic['message'] = obj.site_message
        dic['status'] = obj.status
        status.append(dic)
    return JsonResponse({
        'status': status
    })


@login_required(login_url='/users/login/')
def get_site(request):
    f_sites = []
    site_ = []
    counter = 1
    for host in request.GET.getlist('host_id[]'):
        print(host)
        site = GetIISSite.objects.get(hosts=host)
        try:
            hostname = site.hosts.all()[0].hostname
            site = eval(site.message)[hostname]['stdout']
            sites = site.split('\r\n')
            for site in sites:
                if counter == 1:
                    site_.append(site.split(' ')[1].strip("\""))
                else:
                    if site.split(' ')[1] in site_:
                        site_.append(site.split(' ')[1].strip("\""))
                    else:
                        pass
            counter += 1
        except Exception as e:
            pass
    try:
        site__ = set(site_)
        for each_b in site__:
            count = 0
            for each_a in site_:
                if each_b == each_a:
                    count += 1
            if count >= 2:
                f_sites.append(each_b)
        if len(f_sites) == 0:
            f_sites = site_
    except Exception as e:
        pass
    return JsonResponse({
        'site': f_sites
    })


def manual_get_site(request):
    Manual_get_iis_site.delay()
    return JsonResponse({
        'statues': 1
    })