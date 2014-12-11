from django.conf.urls import patterns, url
from randomdate import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^view_results$', views.view_results, name='view_results'),
        url(r'^viewresults$', views.view_results, name='view_results'),
        url(r'^finddate$', views.find_date, name='find_date'),
        url(r'^find_date$', views.find_date, name='find_date'))
