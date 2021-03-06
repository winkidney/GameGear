#coding:utf-8
#GearAnswer/views.py
#2014.05.14


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.contrib.auth import (authenticate, login, logout)
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


from UCenter.apis import user_exist,logined
from GearAnswer.forms import (RegisterForm,LoginForm,UserProfileForm,
                              clean_err_form,NewTopicForm,
                              ReplyFrom)
from GearAnswer.apis import *


from GearAnswer.config import ANSWER_ROOT as ROOT_URL 





def test_view(request):
    #todo : i18n test
    return HttpResponse(_(u"You have already logined!"))

def home_view(request):
    navigations = get_navs()
    node_list = get_node_list()
    hot_topics = get_today_hot()
    hot_nodes = get_hotnodes()
    new_nodes = get_newnodes()
    return render_template(request, 'gearanswer/base.html',
                              locals(),
                              )
    
    
def nav_view(request, nav_id, *args, **kwargs):
    #to display ajax tab view
    page = request.GET.get('page', 1)
    nav = get_nav_byid(nav_id)
    if not nav:
        raise Http404
    nodes = nav.get_children()
    topics = get_topics_bynode(nodes, page)
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
            login_form = LoginForm(request.POST, )
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data.get('username'), 
                                    password=login_form.cleaned_data.get('password'))
                if user and user.is_active:
                        login(request, user)
                        title = _(u"Login succeed!")
                        content = _(u'Maybe you want to:<a href="%sgear/%s/profile/edit/">Edit your profile</a> or go back to <a href="%s">pre-page</a>' \
                                    % (ROOT_URL, user.id, request.GET.get('next')))
                        info = Info(title, content, request.GET.get('next', ROOT_URL))
                        
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
        title = _(u"Logout Succeed!")
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
                data = register_form.cleaned_data.get
                create_user(data('username'), 
                            data('password1'), 
                            data('email'))
                user = authenticate(username=register_form.cleaned_data.get('username'), 
                                    password=register_form.cleaned_data.get('password1'))
                login(request, user)
                
                title = _(u"Register Succeed!")
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
    
def node_view(request, node_name, *args, **kwargs):
    #todo : add like function
    current_node = get_node_byname(node_name)
    page = request.GET.get('page', 1)
    #if the topic create page is stand_alone
    stand_alone = False
    related_nodes = get_related_nodes(current_node)
    if not current_node:
        raise Http404
    topics = get_topics_bynode(current_node, page)
    topic_count = current_node.topic_count
    return render_template(request, 'gearanswer/node.html',
                              locals(),
                              )


@login_required(login_url=ROOT_URL+'login/')      
@transaction.commit_on_success
def update_topic_view(request, node_name, new_topic=True, *args, **kwargs):
    stand_alone = True
    current_node = get_node_byname(node_name)
    if not current_node:
        raise Http404
    if request.method == "POST":
        #new topic processing
        topic_form = clean_err_form(NewTopicForm, 
                                    request.POST, 
                                    )
        if topic_form.is_valid():
            editor = topic_form.cleaned_data.get('editor')
            if editor == 'ue':
                topic_content = topic_form.cleaned_data.get('content_ue')
            elif editor == 'md':
                topic_content = topic_form.cleaned_data.get('content_md')
            else:
                raise PermissionDenied
            if new_topic:
                topic = update_topic(topic_form.cleaned_data.get('title'),
                         editor,
                         topic_content, 
                         node_name, 
                         request.user.id, 
                         )
                #update topic_count in this node
                current_node.topic_count += 1
                current_node.save()
                
                title = _(u"Topic published!")
                content = _(u"Now you will be rediected to your topic page.")
                redirect_url = topic.get_abs_url()
                    
                info = Info(title, content, redirect_url)
                return render_template(request, 'gearanswer/info.html',
                                            locals(),
                                            )
            
    elif request.method == "GET":
        pass
    return render_template(request, 'gearanswer/new_topic.html',
                              locals(),
                              )

@login_required(login_url=ROOT_URL+'login/')
@transaction.commit_on_success
def reply_view(request, article_id, *args, **kwargs):
    #fixed
    topic = get_topic(article_id)
    
    if not topic:
        raise Http404
    
    if request.method == 'POST':
        reply_form = clean_err_form(ReplyFrom, request.POST)
        if reply_form.is_valid() and reply_form.check_value():
            rfd = reply_form.cleaned_data.get
            if rfd('editor') == 'md':
                content = rfd('comment_md')
            elif rfd('editor') == 'ue':
                content = rfd('comment_ue')
            else:
                raise ValueError, "editor type is required!"
            reply = update_reply(rfd('editor'),
                         content,
                         int(article_id),
                         int(request.user.id,) 
                         )
            #update the topic last reply information
            #and update the reply count
            update_topic_property(topic,
                                  last_reply_id=reply.id,
                                  reply_count=topic.reply_count+1,
                                  update_at = datetime.now(),
                                  )
            
            info = Info(_(u"Reply published!"), 
                        _(u"Now you will be redirected to topic page!"), 
                        topic.get_abs_url())
            return render_template(request, 'gearanswer/info.html',
                                            locals(),
                                            )
        else:
            info = Info(_(u"Reply cannot be null!"), 
                        _(u"Now you will be redirected to topic page!"), 
                        topic.get_abs_url())
            return render_template(request, 'gearanswer/info.html',
                                            locals(),
                                            )
    #if the method is GET or other case. user will be rediected to read page.
    redirect_url = topic.get_abs_url()
    return HttpResponseRedirect(redirect_url)

def mark_as_given(request, node_name, given_type):
    pass

def like_node_view(request, node_name, *args, **kwargs):
    #todo : build
    
    pass

@login_required(login_url=ROOT_URL+'login/')
@csrf_exempt
def topic_star_view(request, *args, **kwargs):
    #todo
    pass
    


@login_required(login_url=ROOT_URL+'login/')
@csrf_exempt
def topic_useless_view(request, *args, **kwargs):
    #todo : add user request number control
    if request.method != 'POST':

        raise PermissionDenied

    jrequest = json_loads(request.body)
    result = ''
    description = ''
    if jrequest and jrequest.has_key('topic_id'):
        topic_id = str(jrequest['topic_id'])
        if topic_id.isdigit():
            topic = get_topic(topic_id)
            if topic:
                if mark_topic_useless(topic, request.user.id):
                    result = 'success'
                    description = _(u"You have successfully marked the topic as useless")
                else:
                    result = 'already_marked'
                    description = _(u"You have already marked it!Don't do it again!")
            else:
                result = 'topic_not_exist'
                description = _(u"Given topic does not exist!")
        else:
            result = 'argument_invalid'
            description = _(u"Your topic_id argument is invalid")
    else:
        result = 'data_valid'
        description = _(u"Your json data is invalid")
    return HttpResponse('"{"result":"%s", "description" : "%s"}"' \
                        % (result, description))

def topic_useful_view(request, *args, **kwargs):
    #todo
    return HttpResponse('set useless success')

def user_profile_view(request, uid, *args, **kwargs):
    #todo : change the default data that displays
    uinfo_dict = get_uinfo(uid)
    if not uinfo_dict:
        raise Http404
    return render_template(request, 'gearanswer/user_profile.html',
                              locals(),
                              )
    
@login_required(login_url=ROOT_URL+'login/')
def user_profile_edit_view(request, uid, *args, **kwargs):
    
    uinfo_dict = get_uinfo(uid)
    uid = int(uid)
    if not uinfo_dict:
        raise Http404
    #check if current user is the profie owner.
    if request.user.id != int(uid):
            raise PermissionDenied
        
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        user_profile_form = clean_err_form(UserProfileForm, 
                                           request.POST, 
                                           )
        if user_profile_form.is_valid():
            update_user(uid, request.FILES.get('avatar'),
                        user_profile_form.cleaned_data)
            
            info = Info(_(u'You have successfully change your profile!'),
                        _(u'Now you will be rediected to edit page.'),
                        request.path)
            return render_template(request, 'gearanswer/info.html',
                                        locals(),
                                        )
    return render_template(request, 'gearanswer/edit_user_profile.html',
                              locals(),
                              )
    
def messages_view(request, *args, **kwargs):
    #todo
    return render_template(request, 'gearanswer/messages.html',
                              locals(),
                              )  
    
def read_view(request, article_id, *args, **kwargs):
    article_id = int(article_id)
    topic = get_topic(article_id)
    replys = get_replys(article_id)
    reply_count = len(replys)
    if not topic:
        raise Http404
    update_view_times(topic)
    return render_template(request, 'gearanswer/read.html',
                              locals(),
                              )

def random_view(request):
    topic_id = get_random_topic_id()  
    return HttpResponseRedirect('%sarticles/%s/' % (ANSWER_ROOT, topic_id)) 
    
def building_view(request):
    info = Info(_(u'页面构建中~'),
                _(u'即将跳转到首页'),
                ANSWER_ROOT)
    return render_template(request, 'gearanswer/info.html',
                                        locals(),
                                        )

