# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path

from .. import views

__all__ = ["urlpatterns"]

app_name = "ops"

urlpatterns = [
    # Resource Task url
    path('task/', views.TaskListView.as_view(), name='task-list'),
    path('task/<uuid:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/<uuid:pk>/adhoc/', views.TaskAdhocView.as_view(), name='task-adhoc'),
    path('task/<uuid:pk>/history/', views.TaskHistoryView.as_view(), name='task-history'),
    path('adhoc/<uuid:pk>/', views.AdHocDetailView.as_view(), name='adhoc-detail'),
    path('adhoc/<uuid:pk>/history/', views.AdHocHistoryView.as_view(), name='adhoc-history'),
    path('adhoc/history/<uuid:pk>/', views.AdHocHistoryDetailView.as_view(), name='adhoc-history-detail'),
    path('celery/task/<uuid:pk>/log/', views.CeleryTaskLogView.as_view(), name='celery-task-log'),

    path('command-execution/', views.CommandExecutionListView.as_view(), name='command-execution-list'),
    path('command-execution/start/', views.CommandExecutionStartView.as_view(), name='command-execution-start'),

    path('multitask/file_transfer/', views.multitask_file_transfer.as_view(), name='multitask_file_transfer'),
    path('multitask/file_transfer/up/', views.upload_file, name='multitask_file_transfer_up'),
    path('multitask/file_transfer/getstatus/', views.get_upstatus, name='multitask_file_transfer_status'),

    path('play/createjobtemplates/', views.createjobtemplates, name='iis_job'),
    path('play/createjobtemplates/getstatus/', views.get_iisstatus, name='iis_job_status'),
    path('play/createwebsite/', views.createwebsite, name='iis_create_website'),
    path('play/createwebsite/getstatus/', views.get_ciisstatus, name='iis_create_status'),
    path('play/getsite/', views.get_site, name='iis_getsite'),
    path('play/manualgetsite/', views.manual_get_site, name='iis_manual_getsite'),

    path('crontab/create/', views.crontabcreateview, name='crontab-create'),
    path('crontab/getstatus/', views.getstatus, name='crontab-getstatus'),
    path('crontab/remove/', views.removecrontabtask, name='crontab-remove'),
    path('crontab/view/', views.crontablistview, name='crontab-getlist'),
    path('crontab/update/<str:host_id>/', views.crontabupdate, name='crontab-update'),
]
