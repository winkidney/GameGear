#coding:utf-8
#GearAnswer/apis.py - api collections of the site.
#ver 0.1 - by winkidney - 2014.05.13

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.exceptions import  ObjectDoesNotExist
import logging

from UCenter.models import User
from GearAnswer.models import Topic,Node
from UCenter.apis import get_user_by_id
def get_node(node_name):
    "Get a Node object by its name,return Node instance if successfully done,False if failed"
    try:
        node = Node.objects.get(name=node_name)
    except ObjectDoesNotExist:
        logging.warn("Node object [%s] does not existed!" % node_name)
        return False
    return node

def get_topic(topic_id):
    "Get a Topic object by its id,return Node instance if successfully done,False if failed"
    try:
        topic = Topic.objects.get(id=topic_id)
    except ObjectDoesNotExist:
        logging.warn("Topic object [%s] does not existed!" % topic_id)
        return False
    return topic

def update_avatar(avatar, avatar_file):
    """ avatar is a models.ImageField instance,
        avatar_file is the file object from html form's file-input-filed.
        If successfully updated, return True.
    """
    image = avatar_file
    if image:
        if avatar:
            avatar.delete()
        file_ext = image.name.split('.')[1]
        avatar.save('%s.%s' % (uuid.uuid1(), file_ext), 
                             image)
        return True
    raise ValueError, 'avatar_file %s is not a InMemoryFile instance!' % image

def update_node(name, description, node_avatar=None, pnode=None, avatar=None):
    """ update_node(unicode name, unicode description, 
                    unicode node_avatar, unicode pnode, InMemoryFile avatar=None)
    """
    node = get_node(name)
    if not node:
        node = Node()
    node.name = name
    node.description = description
    # If the node is the first node ,it will be saved to avoid
    # errors from the default parent node setting.
    node.save()
    if node_avatar:
        update_avatar(avatar, node_avatar)
    
    if pnode:
        node.parent = Node.objects.get(name=pnode)
    else:
        node.parent = Node.objects.get(id=1)
    node.save()
    return True
    
    
    
def update_topic(title, editor, content, node_name, uid, topic_id=None):    #to do
    """ create_topic(unicode title, unicode topic, unicode node, int uid)
        Update a topic while create a new topic if the topic_id is given.
        return Topic instance if success, an error will be raised if fail by detail.
    """
    if topic_id:
        topic = get_topic(topic_id)
    else:
        topic = None
    if not topic:
        topic = Topic()
    topic.author = get_user_by_id(uid)
    topic.title = title
    topic.editor = editor
    topic.content = content
    topic.node = get_node(node_name)
    topic.save()
    return topic

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
def is_topic_owner(request, topic_id):    
    if request.id == get_topic.author.id:
        return True
    return False

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
    

