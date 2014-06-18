#!/usr/bin/evn python
#coding:utf-8
#GearAnswer/models.py - models file
#by winkidney - 2014年6月18日

from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.core.exceptions import  ObjectDoesNotExist
from UCenter.models import User,Message
from GearAnswer.config import *

EDITOR_TYPES = (
    ('md', _(u'markdown editor')),
    ('ue', _(u'ueditor')),
)




        
class Node(models.Model):
    
    """Topic Node ,the same as topic Type"""
    class Meta:
        verbose_name_plural = _(u'topic node')
        verbose_name = _(u'topic node ')
      
    name = models.CharField(blank=False, unique=True, 
                            max_length=100, 
                            verbose_name=_(u'node name'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    avatar = models.ImageField(blank=True,
                               upload_to='nodes/', 
                               verbose_name=_(u'node avatar'))
    description = models.TextField(blank=True,
                                   verbose_name=_(u'node description'))
    help_text = models.TextField(blank=True,
                                 verbose_name=_(u"node help text"))
    topic_count = models.IntegerField(blank=False,
                                  default=0, verbose_name=_(u'topic count'))
    parent = models.ForeignKey('Node', 
                               default=0, 
                               blank=False, verbose_name=_(u"parent-node"))
    
    def __unicode__(self):
        
        return self.name
    
    def get_avatar_url(self):
        
        return self.avatar.url
    
    def get_abs_url(self):
        return u"%snode/%s/" % (ANSWER_ROOT, self.name)

class Tag(models.Model):
    
    """Topic tag.Repution is needed for add new tag."""
    
    class Meta:
        verbose_name_plural = _(u'question tag manager')
        verbose_name = _(u'question tag manager')
    
    name = models.CharField(max_length=100, blank=False, verbose_name=_(u'tag name'))
    topic_count = models.IntegerField(blank=False, verbose_name=_(u'question count'))
    
    
    def get_abs_url(self):
        return u"%stags/%s/" % (ANSWER_ROOT, self.name)
    
    def __unicode__(self):
        
        return self.name
    

    
class Topic(models.Model):
    
    """Topic that contains enough info"""
    
    class Meta:
        verbose_name_plural = _(u"topics")
        verbose_name = _(u"topic")
        get_latest_by = "-create_at"
        ordering = ['-update_at']
        
    title = models.CharField(max_length=250, blank=False, 
                             db_index=True,
                             verbose_name=_(u'question title'))
    
    content = models.TextField(blank=True, verbose_name=_(u'topic content'))
    is_question = models.BooleanField(blank=False, default=False, verbose_name=_(u'If it is a question topic'))
    work_out = models.BooleanField(blank=False, default=False, verbose_name=_(u'if the question worked out'))
    editor = models.CharField(max_length=5,
                              blank=False,
                              default='md',
                              choices=EDITOR_TYPES,verbose_name=_(u'topic type')
                              )
    author = models.ForeignKey(User, blank=False, verbose_name=_(u'topic author'))
    reply_count = models.IntegerField(blank=False, default=0, verbose_name=_(u'reply count'))
    
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_(u'updated at'))
    last_reply_id = models.CharField(max_length=15, blank=True, default='0',
                                     verbose_name=_(u"last reply's id"))
    
    
    useful = models.IntegerField(blank=False, default=0, verbose_name=_(u'useful'))
    #todo : 有更好的设计么？
    useful_uids = models.CharField(max_length=UIDS_RESERVE_LENGTH,
                                   blank=True, 
                                   verbose_name=_(u"uids that mark this topic useful."))
    stars = models.IntegerField(blank=False, default=0, verbose_name=_(u'stared count'))
    useless = models.IntegerField(blank=False, default=0, verbose_name=_(u'useless'))
    #todo : 有更好的设计么？
    useless_uids = models.CharField(max_length=UIDS_RESERVE_LENGTH,
                                   blank=True, 
                                   verbose_name=_(u"uids that mark this topic useful."))
    view_times = models.IntegerField(blank=False, default=0, verbose_name=_(u'view times'))
    
    #answers = models.ManyToManyField(Answer, blank=True, verbose_name=_(u'response to the topic'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_(u'topic tags'))
    node = models.ForeignKey(Node, blank=False, verbose_name=_(u'topic node'))
    
    @property
    def last_reply(self):
        if self.last_reply_id != '0':
            try:
                return Reply.objects.get(id=self.last_reply_id)
            except:
                return None
        else:
            return None
    
    def get_abs_url(self):
        return u"%sarticles/%s/" % (ANSWER_ROOT, self.id)
    
    def __unicode__(self):
        
        return self.title
    
    def check_digit_input(self, value):
        "check if the input value is digit.Return value if True."
        if not isinstance(value, (int,str,unicode)):
            raise TypeError,"value [%s] must be an int/str/unicode type object" % value
        value = str(value)
        if not value.isdigit():
            raise TypeError,'value [%s] must be digit.' % value
        return value
    
    def in_useful(self, uid):
        "Check if the given uid in the useful_uids,return True or false"
        uid = self.check_digit_input(uid)
        uids = self.useful_uids.split('_')
        self.useful_checked = True
        if str(uid) in uids:
            return True
        else:
            return False
        
        
    def insert_useful_uid(self, uid):
        try:
            self.useful_checked
        except:
            raise NotImplementedError,"You must call in_useful function first before call this."
        uid = self.check_digit_input(uid)
        uids = self.useful_uids.split('_')
        while len(self.useful_uids) > UIDS_MAX_LENGTH:
            uids = self.useful_uids.split('_')
            uids.pop(0)
            self.useful_uids = '_'.join(uids)
        uids.append(uid)
        self.useful_uids = '_'.join(uids)
        self.save()
        del self.useful_checked

class Reply(models.Model):
    
    """Answer for Question"""
    
    class Meta:
        verbose_name_plural = _(u"replys")
        verbose_name = _(u"reply")
        get_latest_by = "-create_at"
        ordering = ['create_at']
    
    editor = models.CharField(max_length=5,
                              blank=False,
                              default='md',
                              choices=EDITOR_TYPES,verbose_name=_(u'editor')
                              )    
    content = models.TextField(blank=False, verbose_name=_(u'reply content'))
    author = models.ForeignKey(User, blank=False, 
                               db_index=True,
                               verbose_name=_(u'reply author'))
    is_best = models.BooleanField(default=False, verbose_name=_(u'is right answer'))
    useful = models.IntegerField(blank=False, default=0, verbose_name=_(u'useful'))
    useless = models.IntegerField(blank=False, default=0, verbose_name=_(u'useless'))
    
    topic = models.ForeignKey(Topic,blank=False,verbose_name=_(u'topic'))
    
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(u'updated at'))
    
    def __unicode__(self):
        
        return u'%s - %s' %(self.id, self.topic.title)


class UserProfile(models.Model):
    
    """Question Node ,the same topic Type"""
    class Meta:
        verbose_name_plural = _(u'users profile')
        verbose_name = _(u'user profile ')
        
    user = models.OneToOneField(User, blank=False, verbose_name="profile owner")
    fav_topics = models.ManyToManyField(Topic,
                                       blank=True, 
                                verbose_name=_(u"user's favorite's nodes count") )
    fav_nodes = models.ManyToManyField(Node,
                                      blank=True, 
                                      verbose_name=_(u"user's favorite nodes's count")) 
    fav_users = models.ManyToManyField(User,related_name="fav_user",
                                      blank=True,
                                      verbose_name=_(u"user's caring-user count"))
    
    gears = models.IntegerField(blank=False, default=DEFAULT_GEARS, verbose_name=_(u'gears'))
    reputation = models.IntegerField(blank=False, default=0, 
                                     verbose_name=_(u"reputation in GameGear"))
    
    def __unicode__(self):
        return "%s %s" % (self.user.id, self.user)
    
    def unread_msg_count(self):
        #todo : add msg_get function
        pass


#settings start
class Nav(models.Model):
    
    """Nav tabs from Tag,The data to generate nav menu"""
    class Meta:
        verbose_name_plural = _(u'Navigations')
        verbose_name = _(u'Navigation')
        ordering = ['display_order']
        
    name = models.CharField(max_length=50, verbose_name=_(u'Navigation name'))
    display_order = models.IntegerField(blank=False, default=0, verbose_name=_(u'display order'))
    child_nodes = models.ManyToManyField(Node,verbose_name=_(u'nav child-nodes'))
    
    def __unicode__(self):
        return u"%s" % self.name

    def get_children(self):
        return self.child_nodes.all()
        
class Setting(models.Model):
    
    """global settings of the website"""
    
    class Meta:
        verbose_name_plural = _(u"global settings")
        verbose_name = _(u'global settings')
        ordering = ['variable']
        
    variable = models.CharField(max_length=30, verbose_name=_(u'setting variable'))
    value = models.CharField(max_length=100, verbose_name=u'setting value')

    def __unicode__(self):
        return u"%s" % (self.variable)

    