#!/usr/bin/evn python
#coding:utf-8
#GearAnswer/models.py - models file
#by winkidney - ver 0.1
#2014

from django.db import models
from django.utils.translation import ugettext_lazy as _
from UCenter.models import User


    
class Node(models.Model):
    
    """Question Node ,the same topic Type"""
    class Meta:
        verbose_name_plural = _(u'topic node manager')
        verbose_name = _(u'topic node manager')
      
    name = models.CharField(max_length=100, blank=False, verbose_name=_(u'node name'))
    node_img = models.CharField(max_length=250, verbose_name=_(u"node image path"))
    description = models.TextField(verbose_name=_(u'node description'))
    q_count = models.IntegerField(blank=False, verbose_name=_(u'topic count'))


class Tag(models.Model):
    
    """Question tag.Repution is needed for add new tag."""
    
    class Meta:
        verbose_name_plural = _(u'question tag manager')
        verbose_name = _(u'question tag manager')
    
    name = models.CharField(max_length=100, blank=False, verbose_name=_(u'tag name'))
    q_count = models.IntegerField(blank=False, verbose_name=_(u'question count'))
    
    def __unicode__(self):
        
        return self.name
    
class Answer(models.Model):
    
    """Answer for Question"""
    
    class Meta:
        verbose_name_plural = _(u"answer manager")
        verbose_name = _(u"answer manager")
        
    content = models.TextField(blank=False, verbose_name=_(u'question content'))
    author = models.ForeignKey(User, blank=False, 
                               db_index=True,
                               verbose_name=_(u'question author'))
    right = models.BooleanField(default=False, verbose_name=_(u'is right answer'))
    useful = models.IntegerField(blank=False, default=0, verbose_name=_(u'useful'))
    stared = models.IntegerField(blank=False, default=0, verbose_name=_(u'stared'))
    useless = models.IntegerField(blank=False, default=0, verbose_name=_(u'useless'))
    
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(u'updated at'))
    
    def __unicode__(self):
        
        return self.create_at
    
class Question(models.Model):
    
    """Question that contains enough info"""
    
    class Meta:
        verbose_name_plural = _(u"question manager")
        verbose_name = _(u"question manager")
        
    title = models.CharField(max_length=250, blank=False, 
                             db_index=True,
                             verbose_name=_(u'question title'))
    content = models.TextField(blank=False, verbose_name=_(u'question content'))
    author = models.ForeignKey(User, blank=False, verbose_name=_(u'question author'))
    answer_count = models.IntegerField(blank=False, default=0, verbose_name=_(u'answer count'))
    
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(u'updated at'))
    work_out = models.BooleanField(blank=False, default=False, verbose_name=_(u'if the question worked out'))
    useful = models.IntegerField(blank=False, default=0, verbose_name=_(u'useful'))
    stared = models.IntegerField(blank=False, default=0, verbose_name=_(u'stared'))
    useless = models.IntegerField(blank=False, default=0, verbose_name=_(u'useless'))
    view_times = models.IntegerField(blank=False, default=0, verbose_name=_(u'view times'))
    
    tags = models.ManyToManyField(Tag, blank=False, verbose_name=_(u'question tags'))
    Node = models.ForeignKey(Node, blank=False, verbose_name=_(u'question type'))
    
    def __unicode__(self):
        
        return self.title

#settings start
class Nav(models.Model):
    
    """Nav tabs from Tag,The data to generate nav menu"""
    class Meta:
        verbose_name_plural = _(u'nav setting')
        verbose_name = _(u'nav setting')
    
    name = models.CharField(max_length=100, verbose_name=_(u'Nav setting'))
    display_order = models.IntegerField(blank=False, default=0, verbose_name=_(u'display order'))
    Node = models.ManyToManyField(Node, verbose_name=_(u'nav node'))

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

    