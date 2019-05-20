from django.urls import path
from .import views


app_name = 'awx'

urlpatterns = [
    path('list/', views.AwxTaskList.as_view(), name='awx_list'),
    path('run/', views.AwxRun.as_view(), name='awx_run'),
    path('stop/', views.AwxStop.as_view(), name='awx_stop')
]