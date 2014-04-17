#!/usr/bin/env python
#coding:utf-8
'''
UCenter.models -- shortdesc
@author:     winkidney
@contact:    winkidney@gmail.com
@deffield    updated: Updated
'''

__all__ = []
__version__ = 0.1
__date__ = '2014-04-14'
__updated__ = '2014-04-14'

from django.utils.translation import ugettext as _

from django.contrib.auth.models import User 
from django.db import models

from GearArt.models import Collection,Post,PComment


class Message(models.Model):
    
    """message from a user to another
       max number for every user
    """
    
    message = models.TextField(verbose_name=u'message')
    isread = models.BooleanField(verbose_name=u'isread')
    send_time = models.DateTimeField(auto_now_add=True,verbose_name=_(u'send_time'))
    
    
class Gear(models.Model):
    
    """User models extending."""
    
    class Meta:
        verbose_name_plural = u"Gear信息"
        verbose_name = u"Gear信息"
        
    user = models.OneToOneField(User)
    weibo_token = models.CharField(verbose_name=u'微博token',max_length=50, blank=True)
    gears = models.IntegerField(blank=False)    #积分，发主题,回复主题可以获得
    messages = models.ManyToManyField(Message,verbose_name=_(u'messages'))
    
    #private info
    age = models.IntegerField()
    job = models.CharField(max_length=30)
    
    #GameArt
    posts = models.ManyToManyField(Post, verbose_name=_(u'posts'))
    own_collections = models.ManyToManyField(Collection, verbose_name=_(u'collections'))
    #ref_collections = models.ManyToManyField(Collection, verbose_name=_(u'collections'))
    pcomments = models.ManyToManyField(PComment, verbose_name=_(u'comments')) 

    reputation = models.IntegerField(blank=False)   #积分，主题被评分可以获得
    
    #Exchange部分
    e_reputation = models.IntegerField(blank=False, verbose_name=u'E_reputation')
    #questions
    #anwsers
    
    

