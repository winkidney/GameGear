#coding:utf-8
#GearAnswer/apis.py - api collections of the site.
#ver 0.1 - by winkidney - 2014.05.13

from django.utils.html import remove_tags
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.exceptions import  ObjectDoesNotExist
from django.core.files.images import ImageFile
import logging
import uuid

from UCenter.models import User
from GearAnswer.models import Topic,Node,Reply,UserProfile
from UCenter.apis import get_user_by_id
from UCenter.apis import create_user as uc_create_user

def remove_xss_tags(html):
    """"escape the specified html tags from user's content"""
    return remove_tags(html, 'script html body')

def get_node(node_name):
    "Get a Node object by its name,return Node instance if successfully done,False if failed"
    try:
        node = Node.objects.get(name=node_name)
    except ObjectDoesNotExist:
        logging.info("Node object [%s] does not existed!" % node_name)
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

def get_replys(topic_id):
    """ Get a topic's reply by topic id.
        Return a list contains query result.
        if topic id is not a int , raise a type error.
    """
    if not isinstance(topic_id, int):
        raise TypeError,"Local var topic id %s is not a int instance" % topic_id
    return Reply.objects.filter(topic_id=topic_id)

def get_reply(reply_id):
    "Get a reply by its id.Return None if not exists."
    try:
        reply = Reply.objects.get(id=reply_id)
    except ObjectDoesNotExist:
        logging.warn("Reply object [%s] does not existed!" % reply_id)
        return None
    return reply
    
    
def update_avatar(avatar, avatar_file):
    """ avatar is a models.ImageField instance,
        avatar_file is the file object from html form's file-input-filed.
        If successfully updated, return True.
    """
    if isinstance(avatar_file, ImageFile):
        raise ValueError, 'avatar_file %s is not a InMemoryFile instance!' % avatar_file
    if avatar:
        avatar.delete()
    file_ext = avatar_file.name.split('.')[1]
    avatar.save('%s.%s' % (uuid.uuid1(), file_ext), 
                             avatar_file)
    return True
    

def create_user(username, password, email):
    
    """ Create a user with its GearAnswer profile.
        Return user,profile if succeed.
    """
    
    user = uc_create_user(username, password, email)
    profile = UserProfile()
    profile.user = user
    profile.save()
    return user,profile
    

def update_user(uid, avatar_file, profile_dict):
    """ Update a user profile by all the editable attributes.
        update_user()
    """
    #to test
    if not isinstance(profile_dict, dict):
        raise TypeError, "Profile dict [%s] is not a instance of dict!" % profile_dict
    if not isinstance(uid, int):
        raise TypeError, "uid [%s] must be an int instance!" % uid
    user = get_user_by_id(uid)
    
    #update avatar
    #if not isinstance(avatar_file, ImageFile):
    #    raise ValueError, 'avatar_file %s is not a InMemoryFile instance!' % avatar_file
    for item in profile_dict.items():
        if item[0] != u'avatar':
            user.__setattr__(item[0], item[1])
        
    if avatar_file:        
        if user.avatar:
            user.avatar.delete()
        file_ext = avatar_file.name.split('.')[1]
        user.avatar.save('%s.%s' % (uuid.uuid1(), file_ext), 
                                 avatar_file)
    
    
    
    user.save()
    return user

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
    topic.content = remove_xss_tags(content)
    topic.node = get_node(node_name)
    topic.save()
    return topic

def update_reply(editor, content, article_id, uid, reply_id=None):
    """ Create or update a reply.
        update_reply(unicode content,int article_id, int uid, int reply_id)
        If reply id does not exist,the function will create a new one.
    """
    #tofix
    if not isinstance(article_id, int):
        raise TypeError, "article_id %s is not a int object" % article_id
    if reply_id:
        if isinstance(reply_id, int):
            raise TypeError, "reply_id %s is not a int object" % article_id
        reply = get_reply(reply_id)
    else:
        reply = Reply(content=content,
                      topic=Topic.objects.get(id=article_id),
                      author=User.objects.get(id=uid)
                      )
        reply.save()
    
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
                      'id': int(uid),
                      'detail' : (
                          (_(u'Uid'), user.id),
                          
                          (_(u'Username'), user.name),
                          (_(u'Email'), user.email),
                          (_(u'Self description'), user.description),
                          (_(u'Good at'), user.good_at),
                          (_(u'Interests'), user.interests),
                          (_(u'Website'), user.website),
                        ),
                            'avatar' : avatar_url,
                            'username' : user.name,
                            'email' : user.email,
                            'description' : user.description,
                            'good_at' : user.good_at,
                            'interests' : user.interests,
                            'website' : user.website,
                            'create_at' : user.created_at,
                      }
    #GearAnswer profile
    profiles = UserProfile.objects.filter(user_id=uid)
    if profiles:
        profile = profiles[0]
        user_info_dict['gears'] = profile.gears
        user_info_dict['ftopic_count'] = profile.ftopic_count
        user_info_dict['fnode_count'] = profile.fnode_count
        user_info_dict['fuser_count'] = profile.fuser_count
        user_info_dict['unread_msg_count'] = profile.fuser_count
    return user_info_dict

  

