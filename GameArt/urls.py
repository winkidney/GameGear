#coding:utf-8
#urls.py of GameArt
from django.conf.urls import patterns, include, url
import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'', views.home),
    
    # Examples:
    # url(r'^$', 'gamegear.views.home', name='home'),
    # url(r'^gamegear/', include('gamegear.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
