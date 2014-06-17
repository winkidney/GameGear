#!/usr/bin/evn python
#coding:utf-8
#GearAnswer/models.py - models file
#by winkidney - ver 0.1
#2014

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import  ObjectDoesNotExist
from UCenter.models import User

EDITOR_TYPES = (
    ('md', _(u'markdown editor')),
    ('ue', _(u'ueditor')),
)

class UserProfile(models.Model):
    
    """Question Node ,the same topic Type"""
    class Meta:
        verbose_name_plural = _(u'users profile')
        verbose_name = _(u'user profile ')
        
    user = models.OneToOneField(User, blank=False, verbose_name="profile owner")
    ftopic_count = models.IntegerField(blank=False, default=0, 
                                verbose_name=_(u"user's favorite's nodes count") )
    fnode_count = models.IntegerField(blank=False, default=0, 
                                      verbose_name=_(u"user's favorite nodes's count")) 
    fuser_count = models.IntegerField(blank=False, default=0,
                                      verbose_name=_(u"user's caring-user count"))
    unread_msg_count = models.IntegerField(blank=False, default=0,
                                      verbose_name=_(u"user's caring-user count"))
    gears = models.IntegerField(blank=False, default=0, verbose_name=_(u'gears'))

class Node(models.Model):
    
    """Topic Node ,the same as topic Type"""
    class Meta:
        verbose_name_plural = _(u'topic node')
        verbose_name = _(u'topic node ')
      
    name = models.CharField(blank=False, unique=True, 
                            max_length=100, 
                            verbose_name=_(u'node name'))
    avatar = models.ImageField(blank=True,
                               upload_to='nodes/', 
                               verbose_name=_(u'node avatar'))
    description = models.TextField(blank=True,
                                   verbose_name=_(u'node description'))
    help_text = models.TextField(blank=True,
                                 verbose_name=_(u"node help text"))
    q_count = models.IntegerField(blank=False,
                                  default=0, verbose_name=_(u'topic count'))
    parent = models.ForeignKey('Node', 
                               default=0, 
                               blank=False, verbose_name=_(u"parent-node"))
    
    def __unicode__(self):
        
        return self.name
    
    def get_avatar_url(self):
        
        return self.avatar.url
    
    def get_abs_url(self):
        return u"/node/%s/" % self.name

class Tag(models.Model):
    
    """Topic tag.Repution is needed for add new tag."""
    
    class Meta:
        verbose_name_plural = _(u'question tag manager')
        verbose_name = _(u'question tag manager')
    
    name = models.CharField(max_length=100, blank=False, verbose_name=_(u'tag name'))
    q_count = models.IntegerField(blank=False, verbose_name=_(u'question count'))
    
    
    def get_abs_url(self):
        return """/tags/%s/""" % self.name
    
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
    
    work_out = models.BooleanField(blank=False, default=False, verbose_name=_(u'if the question worked out'))
    useful = models.IntegerField(blank=False, default=0, verbose_name=_(u'useful'))
    stars = models.IntegerField(blank=False, default=0, verbose_name=_(u'stared count'))
    useless = models.IntegerField(blank=False, default=0, verbose_name=_(u'useless'))
    
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
        return """/articles/%s/""" % self.id
    
    def __unicode__(self):
        
        return self.title
    
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

#settings start
class Nav(models.Model):
    
    """Nav tabs from Tag,The data to generate nav menu"""
    class Meta:
        verbose_name_plural = _(u'nav setting')
        verbose_name = _(u'nav setting')
    
    name = models.CharField(max_length=100, verbose_name=_(u'Nav setting'))
    display_order = models.IntegerField(blank=False, default=0, verbose_name=_(u'display order'))
    Nodes = models.ManyToManyField(Node, verbose_name=_(u'nav child-nodes'))
    
    def __unicode__(self):
        return self.name
    
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

    