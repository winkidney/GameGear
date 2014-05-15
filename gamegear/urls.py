#coding:utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import GearAnswer
admin.autodiscover()

#import xadmin
#xadmin.autodiscover()
# version模块自动注册需要版本控制的 Model
#from xadmin.plugins import xversion
#xversion.register_models()

urlpatterns = patterns('',
    #url(r'xadmin/', include(xadmin.site.urls)),
    
    # Examples:
    # url(r'^$', 'gamegear.views.home', name='home'),
    # url(r'^gamegear/', include('gamegear.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('GearAnswer.urls')),
)
