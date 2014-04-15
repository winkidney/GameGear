#!/usr/local/bin/python2.7
#coding:utf-8
'''
UCenter.models -- shortdesc

UCenter.models is a description

It defines classes_and_methods

@author:     winkidney
@contact:    winkidney@gmail.com
@deffield    updated: Updated
'''

__all__ = []
__version__ = 0.1
__date__ = '2014-04-14'
__updated__ = '2014-04-14'

from django.contrib.auth.models import User 
from django.db import models

class Gear(models.Model):
    """User models extending."""
    user = models.OneToOneField(User)
    weibo_token = models.CharField(verbose_name=u'微博token',max_length=50, blank=True)
    
    gears = models.IntegerField(blank=False)    #积分，发主题,回复主题可以获得
    #GameArt 部分
    reputation = models.IntegerField(blank=False)   #积分，主题被评分可以获得
    
    #Exchange部分
    e_reputation = models.IntegerField(blank=False, verbose_name=u'E_reputation')
    
    class Meta:
        verbose_name_plural = u"Gear信息"
        verbose_name = u"Gear信息"
        

    