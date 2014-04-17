#!/usr/bin/env python
#coding:utf-8
#GameArt/models.py - models of GameGear
from django.utils.translation import gettext_lazy as glt
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User

#from UCenter.models import Gear


class License(models.Model):
    
    """Type of the art masterpieces"""
    
    class Meta:
        verbose_name_plural = u"license"
        verbose_name = u"license"
        
    name = models.CharField(max_length=250, verbose_name=u'name')
    link = models.URLField()
    img_url = models.URLField()

class ArtType(models.Model):
    
    """Type of the art masterpieces"""
    
    class Meta:
        verbose_name_plural = u"Type"
        verbose_name = u"Type"
        
    name = models.CharField(max_length=250, verbose_name=u'name')
    display_order = models.IntegerField(verbose_name=u'display order')
    
class Tag(models.Model):
    
    """tags of the art masterpieces"""
    
    class Meta:
        verbose_name_plural = u"Tags"
        verbose_name = u"Tag"
        
    name = models.CharField(max_length=250,verbose_name='name')
    
class PostType(models.Model):
    
    """ Post type of the art masterpiece.
        For example: 2d art,3d art,sound effects etc
    """
    
    class Meta:
        verbose_name_plural = u"post type"
        verbose_name = u"post type"
        
    name = models.CharField(max_length=250)
    display_order = models.IntegerField()

class Art(models.Model):
    
    """Art masterpiece belong a post or a comment.
       The file path is reative to the media_root in  settings file
    """
    
    class Meta:
        verbose_name_plural = u"arts"
        verbose_name = u"art"
    
    filepath = models.CharField(max_length='250',verbose_name=u'filepath')
    size = models.IntegerField(verbose_name=u'size')
    down_times = models.IntegerField(verbose_name=u'down_times')
    tags = models.ManyToManyField(Tag, verbose_name=u'tags')
    type = models.ForeignKey(ArtType, verbose_name=u"type")

class PComment(models.Model):
    
    """ Posts'comment of the art masterpiece."""
    
    class Meta:
        verbose_name_plural = u"comments"
        verbose_name = u"comment"
    ownerid = models.CharField(max_length=50,blank=False) #author uid
    content = models.TextField(blank=False,verbose_name=u'content')
    rating = models.IntegerField(blank=False, verbose_name='rating')   #帖子评分
    arts = models.ManyToManyField(Art, verbose_name=u"art")
    reply_to = models.ForeignKey('self', verbose_name=_(u'reply to'), blank=True)     #父回复
    
    
class Post(models.Model):
    
    """ Posts of the art masterpiece."""
    
    class Meta:
        verbose_name_plural = u"post"
        verbose_name = u"post"
    
        
    title = models.CharField(max_length=250, blank=False, verbose_name=u'title')
    
    authors = models.CharField(max_length=250,)
    content = models.TextField(blank=False, verbose_name=u'content')
    rating = models.IntegerField(blank=False, verbose_name=u'rating')   #帖子评分
    
    view_times = models.IntegerField(blank=False, verbose_name=u'viewed times')
    rating_times = models.IntegerField(blank=False, verbose_name=u'rating times')
    masterpiece = models.BooleanField(verbose_name=u'masterpiece')
    
    post_time = models.DateTimeField(auto_now_add=True, verbose_name=u'post time')
    modify_time = models.DateTimeField(auto_now=True, verbose_name=u'modify time')
    
    license = models.ManyToManyField(License, verbose_name=u'license')
    tags = models.ManyToManyField(Tag, verbose_name=glt('tag'))
    comments = models.ManyToManyField(PComment, verbose_name=u'comment')
    
    content_type = models.ForeignKey(PostType, verbose_name=_(u'type'))
    
    #包含的文件
    arts = models.ManyToManyField(Art, verbose_name=u"art")

class Collection(models.Model):
    
    """tags of the art masterpieces"""
    
    class Meta:
        verbose_name_plural = u"collections"
        verbose_name = u"collection"     
    
    name = models.CharField(max_length=250, verbose_name=u'art')
    posts = models.ManyToManyField(Post,verbose_name=u'art')
    description = models.TextField(verbose_name=u"description")
    content = models.TextField(verbose_name=u'content')
    
    author = models.ManyToManyField(Gear,verbose_name=_('collection author'))
    
    rating = models.IntegerField(blank=False, verbose_name=u'rating')   #帖子评分
    comments = models.ManyToManyField(PComment, verbose_name=u'comment')  
    
    post_time = models.DateTimeField(auto_now_add=True, verbose_name=u'post time')
    modify_time = models.DateTimeField(auto_now=True, verbose_name=u'modify time')   
    
    star_count = models.IntegerField(verbose_name=_(u'star count'))
    
         
        

    

        
        
        
        
        
        