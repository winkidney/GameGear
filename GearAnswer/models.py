#!/usr/bin/evn python
#coding:utf-8
#GearAnswer/models.py - models file
#by winkidney - ver 0.1
#2014

from django.db import models
from django.utils.translation import ugettext_lazy as _
from UCenter.models import User

class Type(models.Model):
    
    """Question type and tag type"""
    
    name = models.CharField(max_length=100, blank=False, verbose_name=_(u'type name'))
    q_count = models.IntegerField(blank=False, verbose_name=_(u'question count'))

class Tag(models.Model):
    
    """Question tag.Repution is needed for add new tag."""
    
    class Meta:
        verbose_name_plural = _(u'question tag')
        verbose_name = _(u'question tag')
    
    name = models.CharField(max_length=100, blank=False, verbose_name=_(u'tag name'))
    q_count = models.IntegerField(blank=False, verbose_name=_(u'question count'))
    
    def __unicode__(self):
        
        return self.name
    
class Answer(models.Model):
    
    """Answer for Question"""
    
    class Meta:
        verbose_name_plural = _(u"question")
        verbose_name = _(u"question")
        
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
        verbose_name_plural = _(u"question")
        verbose_name = _(u"question")
        
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
    type = models.ForeignKey(Type, blank=False, verbose_name=_(u'question type'))
    
    def __unicode__(self):
        
        return self.title

