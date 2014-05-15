#coding:utf-8
#GearAnswer/views.py
#2014.05.14

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _

def render_template(request, template, data=None):
    "Wrapper around render_to_response that fills in context_instance for you."
    response = render_to_response(template, data,
                              context_instance=RequestContext(request))
    return response

def home_view(request):
    return render_template(request, 'gearanswer/base.html',
                              locals(),
                              )
def read_view(request, article_id, *args, **kwargs):
    
    return render_template(request, 'gearanswer/read.html',
                              locals(),
                              )
def new_topic_view(request, *args, **kwargs):
    
    return render_template(request, 'gearanswer/new_topic.html',
                              locals(),
                              )
def node_view(request, *args, **kwargs):
    
    return render_template(request, 'gearanswer/node.html',
                              locals(),
                              )