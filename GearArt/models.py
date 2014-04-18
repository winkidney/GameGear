#!/usr/bin/env python
#coding:utf-8
#GameArt/models.py - models of GameGear
#by winkidney 2014
from django.utils.translation import gettext_lazy as _
from django.db import models
from UCenter.models import User

class License(models.Model):
    
    """Type of the art masterpieces"""
    
    class Meta:
        verbose_name_plural = _(u"license")
        verbose_name = _(u"license")
        
    name = models.CharField(max_length=250, verbose_name=_(u'license name'))
    link = models.URLField(verbose_name=_(u'license url'))
    img_url = models.URLField(verbose_name=_(u'license image url'))
    
    def __unicode__(self):
        return self.name
    
class ArtType(models.Model):
    
    """Type of the art masterpieces"""
    
    class Meta:
        verbose_name_plural = _(u"art type")
        verbose_name = _(u"art type")
        
    name = models.CharField(max_length=250, verbose_name=_(u'art type name'))
    display_order = models.IntegerField(verbose_name=_(u'display order'))
    
    def __unicode__(self):
        return self.name
    
class Tag(models.Model):
    
    """tags of the art masterpieces"""
    
    class Meta:
        verbose_name_plural = _(u"tags")
        verbose_name = _(u"tag")
        
    name = models.CharField(max_length=250, verbose_name=_(u'tag name'))
    
    def __unicode__(self):
        return self.name
    
class PostType(models.Model):
    
    """ Post type of the art masterpiece.
        For example: 2d art,3d art,sound effects etc
    """
    
    class Meta:
        verbose_name_plural = _(u"post types")
        verbose_name = _(u"post type")
        
    name = models.CharField(max_length=250, verbose_name=_(u'post type name'))
    display_order = models.IntegerField(blank=False, verbose_name=_(u'display order'))
    
    def __unicode__(self):
        return self.name
    
class Art(models.Model):
    
    """Art masterpiece belong a post or a comment.
       The file path is reative to the media_root in  settings file
    """
    
    class Meta:
        verbose_name_plural = u"arts"
        verbose_name = u"art"
    
    filepath = models.CharField(max_length='250',verbose_name=_(u'filepath'))
    size = models.IntegerField(verbose_name=_(u'file size'))
    down_times = models.IntegerField(verbose_name=_(u'download times'))
    tags = models.ManyToManyField(Tag, verbose_name=_(u'tags'))
    type = models.ForeignKey(ArtType, verbose_name=_(u"art type"))
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name=_(u'uploda time'))
    
    def __unicode__(self):
        return self.upload_time
    
class PComment(models.Model):
    
    """ Posts'comment of the art masterpiece."""
    
    class Meta:
        verbose_name_plural = _(u"comments")
        verbose_name = _(u"comment")
        
    ownerid = models.ForeignKey(User, max_length=50, blank=False, verbose_name=_(u'comment poster')) #author uid
    content = models.TextField(blank=False,verbose_name=_(u'comment content'))
    rating = models.IntegerField(blank=False, verbose_name=_(u'rating'))   #帖子评分
    reply_to = models.ForeignKey('self', verbose_name=_(u'reply to'), blank=True)     #父回复
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    
    def __unicode__(self):
        return self.name
    
class Post(models.Model):
    
    """ Posts of the art masterpiece."""
    
    class Meta:
        verbose_name_plural = _(u"post")
        verbose_name = _(u"post")
    
        
    title = models.CharField(max_length=250, blank=False, verbose_name=_(u'title'))
    
    starers = models.ManyToManyField(User, verbose_name=_(u'starer'))
    
    content = models.TextField(blank=False, verbose_name=_(u'content'))
    rating = models.IntegerField(blank=False, verbose_name=_(u'rating'))   #帖子评分
    
    view_times = models.IntegerField(blank=False, verbose_name=_(u'viewed times'))
    rating_times = models.IntegerField(blank=False, verbose_name=_(u'rating times'))
    masterpiece = models.BooleanField(verbose_name=_(u'masterpiece'))
    
    post_time = models.DateTimeField(auto_now_add=True, verbose_name=_(u'post time'))
    modify_time = models.DateTimeField(auto_now=True, verbose_name=_(u'modify time'))
    
    license = models.ManyToManyField(License, verbose_name=_(u'license'))
    tags = models.ManyToManyField(Tag, verbose_name=_(u'tag'))
    comments = models.ManyToManyField(PComment, verbose_name=_(u'comment'))
    
    content_type = models.ForeignKey(PostType, verbose_name=_(u'type'))
    
    #包含的文件
    arts = models.ManyToManyField(Art, verbose_name=_(u"art"))
    
    def __unicode__(self):
        return self.title
    
class Collection(models.Model):
    
    """tags of the art masterpieces"""
    
    class Meta:
        verbose_name_plural = _(u"collections")
        verbose_name = _(u"collection")     
    
    name = models.CharField(max_length=250, verbose_name=_(u'art'))
    posts = models.ManyToManyField(Post,verbose_name=_(u'art'))
    description = models.TextField(verbose_name=_(u"description"))
    content = models.TextField(verbose_name=_(u'content'))
    
    starers = models.ManyToManyField(User, verbose_name=_(u'starer'))
    authorid = models.IntegerField(blank=False, verbose_name=_('collection author'))
    
    rating = models.IntegerField(blank=False, verbose_name=_(u'rating'))   #帖子评分
    comments = models.ManyToManyField(PComment, verbose_name=_(u'comment'))  
    
    post_time = models.DateTimeField(auto_now_add=True, verbose_name=_(u'post time'))
    modify_time = models.DateTimeField(auto_now=True, verbose_name=_(u'modify time'))   
    
    star_count = models.IntegerField(verbose_name=_(u'star count'))
    
    def __unicode__(self):
        return self.name     
        

    

        
        
        
        
        
        