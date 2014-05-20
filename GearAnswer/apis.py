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

def get_user(request):
    """get a request and return a user obj"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    return authenticate(username=username, password=password)

def user_exist(username):
    try:
        User.objects.get(name=username)
        return True
    except:
        return False

def logined(request):
    if request.user.is_authenticated():
            return True
    else:
            return False
        
def email_exist(email):
    try:
        User.objects.get(email=email)
        return True
    except:
        return False