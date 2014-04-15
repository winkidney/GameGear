#!/usr/bin/env python
#coding:utf-8
#GemeGear/models.py - models of GameGear
from django.utils.translation import gettext_lazy as glt
from django.db import models
from django.contrib.auth.models import User

    
    

class License(models.Model):
    
    """Type of the art masterpieces"""
    
    class Meta:
        verbose_name_plural = u"license"
        verbose_name = u"license"
        
    name = models.CharField(max_length=250, verbose_name=u'name')
    link = models.URLField()

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
    
    """ Posts of the art masterpiece."""
    
    class Meta:
        verbose_name_plural = u"post"
        verbose_name = u"post"
        
    name = models.CharField(max_length=250)
    display_order = models.IntegerField()

class Art(models.Model):
    
    """Art masterpiece belong a post or a comment."""
    
    class Meta:
        verbose_name_plural = u"arts"
        verbose_name = u"art"
    
    filepath = models.FilePathField(verbose_name=u'filepath')
    size = models.IntegerField(verbose_name=u'size')
    down_times = models.IntegerField(verbose_name=u'')
    tags = models.ManyToManyField(Tag, verbose_name=u'tags')
    type = models.ForeignKey(ArtType, verbose_name=u"type")

class Comment(models.Model):
    
    """ Posts of the art masterpiece."""
    
    class Meta:
        verbose_name_plural = u"comments"
        verbose_name = u"comment"
    ownerid = models.CharField(max_length=50,blank=False) #author uid
    content = models.TextField(blank=False,verbose_name=u'content')
    rating = models.IntegerField(blank=False, verbose_name='rating')   #帖子评分
    arts = models.ManyToManyField(Art, verbose_name=u"art")

class Post(models.Model):
    
    """ Posts of the art masterpiece."""
    class Meta:
        verbose_name_plural = u"post"
        verbose_name = u"post"
        
    title = models.CharField(max_length=250, blank=False, verbose_name=u'title')
    ownerid = models.CharField(max_length=50,blank=False) #author uid
    
    authors = models.CharField(max_length=250,)
    content = models.TextField(blank=False, verbose_name=u'content')
    rating = models.IntegerField(blank=False, verbose_name=u'rating')   #帖子评分
    comments = models.ManyToManyField(Comment, verbose_name=u'comment')
    view_times = models.IntegerField(blank=False, verbose_name=u'viewed times')
    rating_times = models.IntegerField(blank=False, verbose_name=u'rating times')
    masterpiece = models.BooleanField(verbose_name=u'masterpiece')
    
    post_time = models.DateTimeField(auto_now_add=True, verbose_name=u'post time')
    modify_time = models.DateTimeField(auto_now=True, verbose_name=u'modify time')
    
    license = models.ManyToManyField(License, verbose_name=u'license')
    tags = models.ManyToManyField(Tag, verbose_name=glt('tag'))
    #collection = models.ManyToManyField(Collection, verbose_name=u'collection') #集合
    
    type = models.ForeignKey(PostType)
    
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
    
    author = models.ForeignKey(User)
    
    rating = models.IntegerField(blank=False, verbose_name=u'rating')   #帖子评分
    comments = models.ManyToManyField(Comment, verbose_name=u'comment')  
    
    post_time = models.DateTimeField(auto_now_add=True, verbose_name=u'post time')
    modify_time = models.DateTimeField(auto_now=True, verbose_name=u'modify time')        
        

    

        
        
        
        
        
        