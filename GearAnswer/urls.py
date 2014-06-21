#coding:utf-8
#GearAnswer/urls.py
from django.conf.urls import patterns, include, url
from  GearAnswer import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', views.home_view),
    url(r'^ajax/nav/(\d*?)/$', views.nav_view),
    
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^register/$', views.register_view),
    url(r'^input/$', views.building_view),
    
    url(r'^node/(\w*?)/$', views.node_view),
    url(r'^node/(\w*?)/input/$', views.update_topic_view),

    url(r'^gear/(\d)/profile/$', views.user_profile_view),
    url(r'^gear/(\d)/profile/edit/$', views.user_profile_edit_view),    
    url(r'^gear/(\d)/profile/messages/$', views.messages_view),
    url(r'^myaccount/$', views.building_view),
    url(r'^myaccount/favorites/$', views.building_view),

    
    url(r'^articles/(\d*?)/$', views.read_view),
    url(r'^articles/(\d*?)/reply/$', views.reply_view),
    url(r'^random/$', views.random_view),
    
    url(r'^ajax/topic/star/$', views.topic_star_view),
    url(r'^ajax/topic/useful/$', views.topic_useful_view),
    url(r'^ajax/topic/useless/$', views.topic_useless_view),
    
    url(r'^test/$', views.test_view),
    
    
    
    
    # Examples:
    # url(r'^$', 'gamegear.views.home', name='home'),
    # url(r'^gamegear/', include('gamegear.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
