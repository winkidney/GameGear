#!/usr/bin/env python
#coding:utf-8
#GemeGear/models.py - models of GameGear

from django.db import models

class Post(models.Model):
    
    """ Posts of the art masterpiece."""
    class Meta:
        verbose_name_plural = u"主题管理"
        verbose_name = u"主题管理"
        
    title = models.CharField(max_length=250, blank=False, verbose_name=u'标题')
    content = models.TextField(blank=False, verbose_name=u'正文')
    points = models.IntegerField(blank=False, verbose_name=u'评分')   #帖子评分
    comments = models.ManyToManyField(Comment, verbose_name=u'评论')
    view_times = models.IntegerField(blank=False, verbose_name=u'查看次数')
    point_times = models.IntegerField(blank=False, verbose_name=u'评分次数')
    
    license = models.ManyToManyField(License, verbose_name=u'许可')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    collection = models.ManyToManyField(Collection, verbose_name=u'精选集') #集合
    
    arts = models.ManyToManyField(Art, verbose_name=u"素材/资源")
    
    
class Comment(models.Model):
    
    """ Posts of the art masterpiece."""
    
    class Meta:
        verbose_name_plural = u"评论"
        verbose_name = u"评论"
    
    content = models.TextField(blank=False,verbose_name=u'正文')
    points = models.IntegerField(blank=False)   #帖子评分
    arts = models.ManyToManyField(Art, verbose_name=u"素材/资源")
    
class Art(models.Model):
    
    """Art masterpiece belong a post or a comment."""
    
    class Meta:
        verbose_name_plural = u"评论"
        verbose_name = u"评论"
    
    filepath = models.CharField(file)
        
        
        
        
        
        
        
        
        
        
        