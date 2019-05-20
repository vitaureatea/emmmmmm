from django.http import HttpResponse,HttpResponseBadRequest,JsonResponse
from django.views.generic import TemplateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
import requests,simplejson,time

from django.conf import settings

AWX_TOKEN = 'Bearer %s' %settings.AWX_TOKEN


class AwxTaskList( LoginRequiredMixin,TemplateView):
    template_name = 'awx/awx_list.html'

    def get_context_data(self,**kwargs):
        url = settings.AWX_API + "job_templates/"
        headers = {'Authorization': AWX_TOKEN}
        r = requests.get(url, headers=headers)
        payload = r.json()

        context = super().get_context_data(**kwargs)
        context['app'] = 'AWX_Playbook'
        context['templates'] = []
        for template in payload['results']:
            task = {}
            task['name'] = template['name']
            if template['last_job_run']:
                task['last_stime'] = template['last_job_run'].split('.')[0]
            else:
                task['last_stime'] = ""
            task['status'] = template['status']
            task['id'] = template['id']
            print(template['status'])
            context['templates'].append(task)
        print(context['templates'])
        return context


class AwxRun(LoginRequiredMixin,View):

    def get(self, request):
        return HttpResponseBadRequest

    def post(self,request):
        headers = {'Authorization': AWX_TOKEN}
        payload_r = simplejson.loads(request.body)
        template_id = payload_r['templates_id']

        url =  settings.AWX_API + "job_templates/%s/launch/" % template_id
        print('~~~~~',url)
        r = requests.post(url, headers=headers)
        payload_j = r.json()
        print(payload_j)
        job_id = payload_j['id']

        url = settings.AWX_API + "job_templates/%s/" % template_id
        r = requests.get(url, headers=headers)
        payload_ = r.json()
        last_stime = payload_['last_job_run'].split('.')[0]

        while True:
            time.sleep(2)
            url = settings.AWX_API + "jobs/%s/" % job_id
            r = requests.get(url, headers=headers)
            payload_s = r.json()
            if payload_s['status'] == "successful" or payload_s['status'] == "failed":
                job_stauts = payload_s['status']
                break
            elif payload_s['status'] == "canceled":
                job_stauts = "canceled"
                return JsonResponse({
                'awx_status': '',
                'job_stauts': job_stauts,
                'last_stime': last_stime
                })

        url = settings.AWX_API + "jobs/%s/job_events/" % job_id
        r = requests.get(url, headers=headers)
        payload_e = r.json()

        stdout_ = ''
        for job_stdout in payload_e['results']:
            stdout_ +=  " %s \n"  % job_stdout['stdout'].replace('[0;33m','').replace('[0;32m','').replace('[0;31m','').replace('[0m','')


        return JsonResponse({
            'awx_status': stdout_,
            'job_stauts': job_stauts,
            'last_stime': last_stime
        })



class AwxStop(LoginRequiredMixin,View):
    def get(self,request):
        return HttpResponseBadRequest

    def post(self,request):
        headers = {'Authorization': AWX_TOKEN}
        payload_r = simplejson.loads(request.body)
        template_id = payload_r['templates_id']


        url = settings.AWX_API + "job_templates/%s/" % template_id
        r = requests.get(url, headers=headers)
        payload_ = r.json()
        job_id =  payload_['summary_fields']['recent_jobs'][0]['id']
        print(job_id)

        url = settings.AWX_API + "jobs/%s/cancel/"  % job_id
        r = requests.post(url, headers=headers)

        while True:
            time.sleep(2)
            url = settings.AWX_API + "jobs/%s/" % job_id
            r = requests.get(url, headers=headers)
            payload = r.json()
            if payload.get('status') == "canceled":
                job_stauts = payload['status']
                break
            elif payload.get('status') == "successful":
                job_stauts = 'cancel false !'
                break
            elif payload.get('status') == "failed":
                job_stauts = 'cancel false !'
                break

        return JsonResponse({
            'job_stauts': job_stauts,
        })
