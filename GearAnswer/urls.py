#coding:utf-8
#GearAnswer/urls.py
from django.conf.urls import patterns, include, url
from  GearAnswer import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home_view),
    url(r'^articles/(\d*?)/$', views.read_view),
    url(r'^input/$', views.new_topic_view),
    url(r'^node/(\w*?)/$', views.node_view),
    # Examples:
    # url(r'^$', 'gamegear.views.home', name='home'),
    # url(r'^gamegear/', include('gamegear.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
