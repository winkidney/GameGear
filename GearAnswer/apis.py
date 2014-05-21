#coding:utf-8
#GearAnswer/apis.py - api collections of the site.
#ver 0.1 - by winkidney - 2014.05.13
from django.shortcuts import render_to_response
from django.template import RequestContext
from UCenter.models import User

def render_template(request, template, data=None):
    "Wrapper around render_to_response that fills in context_instance for you."
    response = render_to_response(template, data,
                              context_instance=RequestContext(request))
    return response

class Info(object):
    """object for the info page display"""
    
    def __init__(self, title, content, redirect_url=None):
        self.title = title
        self.content = content
        self.redirect_url = redirect_url



