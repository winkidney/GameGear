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
    
class Node(models.Model):
    
    """Question Node ,the same topic Type"""
    class Meta:
        verbose_name_plural = _(u'topic node manager')
        verbose_name = _(u'topic node manager')
      
    name = models.CharField(unique=True, max_length=100, blank=False, verbose_name=_(u'node name'))
    avatar = models.ImageField(upload_to='nodes/', verbose_name=_(u'node avatar'))
    description = models.TextField(verbose_name=_(u'node description'))
    q_count = models.IntegerField(default=0, blank=False, verbose_name=_(u'topic count'))
    parent = models.ForeignKey('Node', default=0, blank=False, verbose_name=_(u"parent-node"))
    
    def __unicode__(self):
        
        return self.name


class Tag(models.Model):
    
    """Question tag.Repution is needed for add new tag."""
    
    class Meta:
        verbose_name_plural = _(u'question tag manager')
        verbose_name = _(u'question tag manager')
    
    name = models.CharField(max_length=100, blank=False, verbose_name=_(u'tag name'))
    q_count = models.IntegerField(blank=False, verbose_name=_(u'question count'))
    
    def __unicode__(self):
        
        return self.name
    

    
class Topic(models.Model):
    
    """Topic that contains enough info"""
    
    class Meta:
        verbose_name_plural = _(u"topic manager")
        verbose_name = _(u"topic manager")
        
    title = models.CharField(max_length=250, blank=False, 
                             db_index=True,
                             verbose_name=_(u'question title'))
    content = models.TextField(blank=False, verbose_name=_(u'topic content'))
    editor = models.CharField(max_length=5,
                              blank=False,
                              default='md',
                              choices=EDITOR_TYPES,verbose_name=_(u'topic type')
                              )
    author = models.ForeignKey(User, blank=False, verbose_name=_(u'topic author'))
    answer_count = models.IntegerField(blank=False, default=0, verbose_name=_(u'reply count'))
    
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(u'updated at'))
    work_out = models.BooleanField(blank=False, default=False, verbose_name=_(u'if the question worked out'))
    useful = models.IntegerField(blank=False, default=0, verbose_name=_(u'useful'))
    stars = models.IntegerField(blank=False, default=0, verbose_name=_(u'stared count'))
    useless = models.IntegerField(blank=False, default=0, verbose_name=_(u'useless'))
    view_times = models.IntegerField(blank=False, default=0, verbose_name=_(u'view times'))
    #answers = models.ManyToManyField(Answer, blank=True, verbose_name=_(u'response to the topic'))
    tags = models.ManyToManyField(Tag, blank=False, verbose_name=_(u'topic tags'))
    node = models.ForeignKey(Node, blank=False, verbose_name=_(u'topic node'))
    
    def get_abs_url(self):
        return """/articles/%s/""" % self.id
    
    def __unicode__(self):
        
        return self.title
    
class Reply(models.Model):
    
    """Answer for Question"""
    
    class Meta:
        verbose_name_plural = _(u"reply manager")
        verbose_name = _(u"reply manager")
        
    content = models.TextField(blank=False, verbose_name=_(u'reply content'))
    author = models.ForeignKey(User, blank=False, 
                               db_index=True,
                               verbose_name=_(u'reply author'))
    is_best = models.BooleanField(default=False, verbose_name=_(u'is right answer'))
    useful = models.IntegerField(blank=False, default=0, verbose_name=_(u'useful'))
    
    useless = models.IntegerField(blank=False, default=0, verbose_name=_(u'useless'))
    
    topic = models.ForeignKey(Topic)
    
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(u'updated at'))
    
    def __unicode__(self):
        
        return self.id

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

    