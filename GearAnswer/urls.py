#coding:utf-8
#GearAnswer/urls.py
from django.conf.urls import patterns, include, url
from  GearAnswer import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', views.home_view),
    url(r'^ajax/tab/(\d*?)/$', views.tab_view),
    
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^register/$', views.register_view),
    
    url(r'^node/(\w*?)/$', views.node_view),
    url(r'^input/$', views.new_topic_view),
    url(r'^reply/$', views.reply_view),
    url(r'^setbest/(\d)/$', views.set_best_view),
    url(r'^setuseless/(\d)/$', views.set_useless_view),
    url(r'^setuseful/(\d)/$', views.set_useful_view),
    url(r'^gear/(\d)/$', views.user_profile_view),
    url(r'^gear/(\d)/edit/$', views.user_profile_edit_view),    
    url(r'^gear/(\d)/messages/$', views.messages_view),
    
    url(r'^articles/(\d*?)/$', views.read_view),
    
    url(r'^test/$', views.test_view),
    
    
    
    
    # Examples:
    # url(r'^$', 'gamegear.views.home', name='home'),
    # url(r'^gamegear/', include('gamegear.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
