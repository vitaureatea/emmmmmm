from django.urls import path
from .import views


app_name = 'doc'

urlpatterns = [
    path('document/', views.docview, name='doc-view'),
    path('document/up/', views.doc_up, name='doc-up'),
    path('document/get/', views.doc_get, name='doc-get'),
    #path('document/checkupdate/', views.check_update, name='doc-checkupdate'),
    path('document/ops_title/', views.get_opsdoc_title, name='opsdoc-title'),
    path('document/ops_body/', views.get_opsdoc_body, name='opsdoc-body'),
    path('document/search/', views.doc_search, name='doc-search'),
]