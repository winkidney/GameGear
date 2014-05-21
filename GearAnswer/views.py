#coding:utf-8
#GearAnswer/views.py
#2014.05.14

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth import (authenticate, login, logout)

from UCenter.apis import user_exist,logined
from GearAnswer.forms import RegisterForm,LoginForm
from GearAnswer.apis import render_template,Info


ROOT_URL = '/'

def home_view(request):
    return render_template(request, 'gearanswer/base.html',
                              locals(),
                              )
def tab_view(request, tab_id, *args, **kwargs):
    
    return render_template(request, 'gearanswer/tab.html',
                              locals(),
                              )
    
def login_view(request, *args, **kwargs):
    if logined(request):
        title = _(u"You have already logined!")
        content = _(u'Maybe you want to: <a href="%slogout/">Logout</a> or go back to <a href="%s">Home</a>' % (ROOT_URL,ROOT_URL))
        info = Info(title, content)
        return render_template(request, 'gearanswer/info.html',
                                        locals(),
                                       )
    else:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data.get('username'), 
                                    password=login_form.cleaned_data.get('password'))
                if user and user.is_active:
                        login(request, user)
                        title = _(u"Login successed!")
                        content = _(u'Maybe you want to:<a href="%sgear/%s/edit/">Edit your profile</a> or go back to <a href="%s">Home</a>' \
                                    % (ROOT_URL, user.id, ROOT_URL))
                        info = Info(title, content)
                        
                        return render_template(request, 'gearanswer/info.html',
                                        locals(),
                                       )   
                else:
                    login_form.errors['username'] = _(u'Username and the password does not match!')
                    
            return render_template(request, 'gearanswer/login.html', 
                                   locals())
                
        elif request.method == 'GET':
            return render_template(request, 'gearanswer/login.html', 
                                   locals())
            
                   


def logout_view(request, *args, **kwargs):
    if logined(request):
        logout(request)
        title = _(u"Logout Successed!")
        content = _(u"Now you will be rediected to home page.")
        redirect_url = ROOT_URL
      
        info = Info(title, content, redirect_url)
    else:
        title = _(u"You have not logined!")
        content = _(u'<a href="%sregister/">Join us now!</a> or <a href="%slogin/">Signin now!</a>' % (ROOT_URL,ROOT_URL))
      
        info = Info(title, content)
    
    return render_template(request, 'gearanswer/info.html',
                                        locals(),
                                        )

def register_view(request, *args, **kwargs):
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            #if form is valid, check the username, username and password.
            if register_form.check_value():
                register_form.save_user()
                user = authenticate(username=register_form.cleaned_data.get('username'), 
                                    password=register_form.cleaned_data.get('password1'))
                login(request, user)
                
                title = _(u"Register Successed!")
                content = _(u"Just enjoy it.Now you will be rediected to home page.")
                redirect_url = ROOT_URL
                
                info = Info(title, content, redirect_url)
                return render_template(request, 'gearanswer/info.html',
                                        locals(),
                                        )
            
        return render_template(request, 'gearanswer/register.html',
                                  locals(),
                                  )
            
    elif request.method == 'GET':
        if logined(request):
            title = _(u"You have logined!")
            content = _(u'<a href="%slogout/">Logout</a> first, Please!' % ROOT_URL)
                
            info = Info(title, content)
            return render_template(request, 'gearanswer/info.html',
                                        locals(),
                                        )
        return render_template(request, 'gearanswer/register.html',
                                  locals(),
                                  )
    
def node_view(request, *args, **kwargs):
    
    return render_template(request, 'gearanswer/node.html',
                              locals(),
                              )
        

def new_topic_view(request, *args, **kwargs):
    
    return render_template(request, 'gearanswer/new_topic.html',
                              locals(),
                              )

def reply_view(request, *args, **kwargs):
    
    return HttpResponse('reply success')

def set_best_view(request, *args, **kwargs):
    return HttpResponse('set best success')

def set_useless_view(request, *args, **kwargs):
    
    return HttpResponse('set useful success')

def set_useful_view(request, *args, **kwargs):
    
    return HttpResponse('set useless success')

def user_profile_view(request, *args, **kwargs):
    
    return render_template(request, 'gearanswer/user_prifile.html',
                              locals(),
                              )
def user_profile_edit_view(request, *args, **kwargs):
    
    return render_template(request, 'gearanswer/user_prifile.html',
                              locals(),
                              )
def messages_view(request, *args, **kwargs):
    
    return render_template(request, 'gearanswer/messages.html',
                              locals(),
                              )  
    
def read_view(request, article_id, *args, **kwargs):
    
    return render_template(request, 'gearanswer/read.html',
                              locals(),
                              )
    
    


