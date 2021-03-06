#coding:utf-8
#GearAnswer/apis.py - api collections of the site.
#ver 0.1 - by winkidney - 2014.05.13

from django.utils.html import remove_tags
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.exceptions import  ObjectDoesNotExist
from django.db.models.query import QuerySet
import logging
import json
from datetime import datetime
import uuid

from UCenter.models import User
from GearAnswer.models import (Topic,Node,Reply,
                               UserProfile,Nav
                               )
from UCenter.apis import get_user_by_id
from UCenter.apis import create_user as uc_create_user
from GearAnswer.config import *

logger = logging.getLogger(__name__)

def json_loads(data):
    try: 
        return json.loads(data)
    except ValueError:
        return None

def remove_xss_tags(html):
    """"escape the specified html tags from user's content"""
    return remove_tags(html, 'script html body')

def get_node_byname(node_name):
    "Get a Node object by its name,return Node instance if successfully done,False if failed"
    try:
        node = Node.objects.get(name=node_name)
    except ObjectDoesNotExist:
        logger.info("Node object [%s] does not existed!" % node_name)
        return False
    return node

def get_node_list():
    """ Get a node list cotains parent and children.
    
    """
    result = []
    pnodes = Node.objects.filter(parent_id=1).exclude(name='none')
    for pnode in pnodes:
        result.append({'parent' : pnode, 
                       'children': Node.objects.filter(parent=pnode)}
                      )
    return result 

def get_newnodes():
    """ Get new nodes depend on its creating time.
        Return a list of them.
    """
    return Node.objects.exclude(name='none').order_by('-create_at')[0:DEFAULT_NEW_COUNT]

def get_hotnodes():
    """ Get hot nodes depend on its total topics (based on its table's data)
        Return a list of them.
    """
    return Node.objects.exclude(name='none').order_by('-topic_count')[0:DEFAULT_HOT_COUNT]

def get_related_nodes(node):
    """
        Get related node by based on its parent.
    """
    if not isinstance(node, Node):
        raise TypeError,"node argument [%s] must be a Node instance!" % node
    return Node.objects.filter(parent=node.parent)

def get_topics_bynode(node, page):
    """ Get topics by node object and return given page's topic list.
        get_topics_bynode(Node node, int/str/unicode page)
    """
    if not isinstance(page, (int,str,unicode)):
        raise TypeError, "page argument [%s] must be a int/str/unicode instance!" \
            % page
    
    if not isinstance(node, (Node, QuerySet)):
        raise TypeError,"node argument [%s] must be a Node instance or QuerySet instance!"\
                % node
    page = int(page)
    topics = Topic.objects.filter(node=node).order_by('-update_at')[(page-1):(page*TOPICS_PER_PAGE_FOR_NODE-1)]
    return topics
    
def get_topic_count_bynode(node):
    """Get topic count by Node object based on Topic table."""
    #todo : add cache here
    if not isinstance(node, Node):
        raise TypeError, "node argument [%s] must be a Node instance!"
    return Topic.objects.filter(node=node).count()
def get_random_topic_id():
    return Topic.objects.order_by('?')[0].id
        
def get_topic(topic_id):
    "Get a Topic object by its id,return Node instance if successfully done,False if failed"
    try:
        topic = Topic.objects.get(id=topic_id)
    except ObjectDoesNotExist:
        logger.warn("Topic object [%s] does not existed!" % topic_id)
        return False
    return topic

def get_today_hot():
    """ Return a list contains DEFAULT_HOT_COUNT's Topic object.
    """
    from datetime import date
    
    topics = Topic.objects.filter(update_at__day=date.today().day).order_by('reply_count')   #.values('id','title','node')
    return topics

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
        logger.warn("Reply object [%s] does not existed!" % reply_id)
        return None
    return reply

def get_navs():
    #todo : add cache
    return Nav.objects.all()

def get_nav_byid(nav_id):
    """get a nav tab by nav_id"""
    #to do : add cache
    if not isinstance(nav_id, (int, str, unicode)):
        raise TypeError,"Local var topic id %s is not a int instance" % nav_id
    try:
        return Nav.objects.get(id=nav_id)
    except ObjectDoesNotExist:
        return None

def create_nav(name, display_order, children):
    """
        create nav by name ,display_order and its child-nodes
    """
    if not isinstance(display_order, (int, str, unicode)):
        raise TypeError,"argument display_order [%s]  is not a int/str/unicode instance" \
            % display_order
    if not isinstance(name, (str, unicode)):
        raise TypeError,"argument name [%s]  is not a int/str/unicode instance" \
            % name
    if not isinstance(children, (Node, QuerySet)):
        raise TypeError,"argument children [%s]  must be  a Node/QuerySet instance" \
            % children
            
    nav = Nav(name=name,
              display_order=display_order,
              )
    nav.save()
    nav.child_nodes.add(children)
    nav.save()
    return nav   
    
def update_avatar(avatar, avatar_file):
    
    """ [avatar] is a models.ImageField instance,
        [avatar_file] is the file object from html form's file-input-filed.
        If successfully updated, return True.
    """
    #if not isinstance(avatar_file, ImageFile):
    #    raise ValueError, 'avatar_file %s is not a InMemoryFile instance!' % avatar_file
    if avatar_file:     
        if avatar:
            avatar.delete()
        file_ext = avatar_file.name.split('.')[1]
        avatar.save('%s.%s' % (uuid.uuid1(), file_ext), 
                                 avatar_file)
        return True
    raise TypeError, "avatar_file argument must be a file object!"
    

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
    if not isinstance(uid, (int,str,unicode)):
        raise TypeError, "uid [%s] must be an int/str/unicode instance!" % uid
    user = get_user_by_id(int(uid))
    
    for item in profile_dict.items():
        if item[0] != u'avatar':
            user.__setattr__(item[0], item[1])
    if avatar_file:       
        update_avatar(user.avatar, avatar_file)

    user.save()
    return user

def update_node(name, description, node_avatar=None, pnode=None, avatar=None):
    """ update_node(unicode name, unicode description, 
                    unicode node_avatar, unicode pnode, InMemoryFile avatar=None)
    """
    node = get_node_byname(name)
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
    return node
    
def update_view_times(topic):
    if not isinstance(topic, Topic):
        raise TypeError, "argument topic [%s] must be a Topic instance!" % topic
    topic.view_times = topic.view_times + 1
    topic.save()


    
def update_topic_property(topic, **kwargs):
    """ Modify Topic object property by keyword arguments
    """
    if not isinstance(topic, Topic):
        raise TypeError,"topic argument [%s] must be a Topic instance!" % topic
    for property in kwargs.items():
        topic.__setattr__(property[0], property[1])
    topic.save()
    return topic
   
def update_topic(title, editor, content, node_name, uid):    
    """ create_topic(unicode title, unicode topic, unicode node, int uid)
        return Topic instance if success, an error will be raised if fail.
    """
    topic = Topic()
    topic.author = get_user_by_id(uid)
    topic.title = title
    topic.editor = editor
    topic.content = remove_xss_tags(content)
    topic.node = get_node_byname(node_name)
    topic.save()
    return topic


def update_reply(editor, content, article_id, uid, reply_id=None):
    """ Create or update a reply.
        update_reply(unicode content,int article_id, int uid, int reply_id)
        If reply id does not exist,the function will create a new one.
    """
    #todo : add modify function
    if not isinstance(article_id, int):
        raise TypeError, "article_id %s is not a int object" % article_id
    if reply_id:
        if isinstance(reply_id, int):
            raise TypeError, "reply_id %s is not a int object" % article_id
        reply = get_reply(reply_id)
    else:
        reply = Reply(content=remove_xss_tags(content),
                      topic=Topic.objects.get(id=article_id),
                      author=User.objects.get(id=uid)
                      )
        
        reply.save()
    return reply
    
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
        avatar_url = user.get_avatar_url
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
                            'create_at' : user.create_at,
                      }
    #GearAnswer profile
    profiles = UserProfile.objects.filter(user_id=uid)
    if profiles:
        profile = profiles[0]
        user_info_dict['gears'] = profile.gears
        user_info_dict['ftopic_count'] = profile.fav_topics.all().count()
        user_info_dict['fnode_count'] = profile.fav_nodes.all().count()
        user_info_dict['fuser_count'] = profile.fav_users.all().count()
        user_info_dict['unread_msg_count'] = profile.unread_msg_count
    return user_info_dict

def check_topic(topic):
    if not isinstance(topic, Topic):
        raise TypeError,"topic [%s] must be a Topic instance!" % topic

def mark_topic_useful(topic, uid):
    "Return True if success, return False is uid existed in useful uids."
    check_topic(topic)
    #todo : decrease user's point
    return topic.insert(uid)

def mark_topic_useless(topic, uid):
    "Return True if success, return False is uid existed in useful uids."
    #todo : decrease user's point
    check_topic(topic)
    if topic.insert_useless_uid(uid):
        topic.useless += 1
        topic.save()
        return True
    else:
        return False

def mark_topic_star(topic, uid):

    "Return True if success, return False if existed."
    check_topic(topic)
    profile = UserProfile.objects.get(user_id=uid)
    if profile.fav_topics.exists(topic):
        return False
    topic.star += 1
    topic.save()
    return True






















