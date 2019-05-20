from django.shortcuts import render
from django.http import JsonResponse
import simplejson
from django.contrib.auth.decorators import login_required

from .models import Doc, OpsDoc


@login_required(login_url='/users/login/')
def docview(request):
    return render(request, 'doc/document.html', {'app': '记录'})



@login_required(login_url='/users/login/')
def doc_up(request):
    payload = simplejson.loads(request.body)
    doc = Doc.objects.get(pk=1)
    update_time = str(doc.update_time).replace('-', '').replace(' ', '').replace('.', '').replace(':', '')

    if payload['last_time'] == update_time:
        doc.doc_value = payload['jsonStr']
        doc.update_user = request.user.username
        doc.save()
        status = '1'
        return JsonResponse({
            'status': status,
        })
    else:
        status = '2'
        update_user = doc.update_user
        return JsonResponse({
            'status': status,
            'update_user': update_user
        })


@login_required(login_url='/users/login/')
def doc_get(request):
    doc = Doc.objects.get(pk=1)
    try:
        dataSource = eval(doc.doc_value)
    except Exception as e:
        dataSource = ''
    last_time = str(doc.update_time).replace('-', '').replace(' ', '').replace('.', '').replace(':', '')

    return JsonResponse({
        'dataSource': dataSource,
        'last_time': last_time
    })


@login_required(login_url='/users/login/')
def get_opsdoc_title(request):
    data = []
    list = OpsDoc.objects.all()
    for obj in list:
        data.append(obj.title)

    return JsonResponse({
        'title': data
    })


@login_required(login_url='/users/login/')
def get_opsdoc_body(request):
    body = OpsDoc.objects.get(title=request.GET.get('title'))
    body = body.content
    return JsonResponse({
        'body': body
    })


@login_required(login_url='/users/login/')
def doc_search(request):

    title = OpsDoc.objects.filter(title__icontains=request.GET.get('search'))
    for obj in title:
        pass
        #暂停
    return JsonResponse({
        'title': request.GET.get('search'),
        'body': '%s的body' % request.GET.get('search')
    })