#coding:utf-8
#GearAnswer/apis.py - api collections of the site.
#ver 0.1 - by winkidney - 2014.05.13
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.exceptions import  ObjectDoesNotExist
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

def get_uinfo(uid):
    """get user info by request object,
       if the user does not exist , return None.
    """
    try:
        user = User.objects.get(id=uid)
    except ObjectDoesNotExist:
        return None
    if user.avatar:
        avatar_url = user.avatar.url
    else:
        avatar_url = None
    user_info_dict = {'avatar' : avatar_url,
                      'detail' : (
                      (_(u'Uid'), user.id),
                      
                      (_(u'Username'), user.name),
                      (_(u'Email'), user.email),
                      (_(u'Self description'), user.description),
                      (_(u'Good at'), user.good_at),
                      (_(u'Interests'), user.interests),
                      (_(u'Website'), user.website),
                      (_(u'Gears'), user.gears),
                      (_(u'Reputation'), user.reputation),
                      ),
                      'detail_dict' : {
                      'uid': user.id,
                      'username' : user.name,
                      'email' : user.email,
                      'description' : user.description,
                      'good_at' : user.good_at,
                      'interests' : user.interests,
                      'website' : user.website,
                      'gears' : user.gears,
                      'reputation' : user.reputation,
                      'create_at' : user.created_at,
                      },
                      'id': int(uid),
                      }
    return user_info_dict
    

