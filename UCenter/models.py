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

from django.utils.translation import ugettext_lazy as _
from django.db import models


from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)

class Message(models.Model):
    
    """message from a user to another.
       max number for every user is 50.
    """
    title = models.CharField(max_length=40, verbose_name=_(u'title'))
    message = models.TextField(verbose_name=_(u'message'))
    isread = models.BooleanField(verbose_name=_(u'is read'))
    send_time = models.DateTimeField(auto_now_add=True,verbose_name=_(u'send_time'))
    
    def __unicode__(self):
        return self.send_time
    
class InterTag(models.Model):
    
    """interests tags of the user """
    
    class Meta:
        verbose_name_plural = _(u"interest tag")
        verbose_name = _(u"major type")
        
    name = models.CharField(max_length=30, verbose_name=_(u'interest tag'))
    count = models.IntegerField(default=0, verbose_name=_(u'person count'))
    
    def __unicode__(self):
        return self.name
    
    
class MajorType(models.Model):
    
    """ Major type of the art masterpiece.
        For example: 2d art,3d art,sound effects etc
    """
    
    class Meta:
        verbose_name_plural = _(u"major type")
        verbose_name = _(u"major type")
        
    name = models.CharField(max_length=250, verbose_name=_(u'major type name'))
    
    def __unicode__(self):
        return self.name
    
class UserManager(BaseUserManager):

    def create_user(self, name, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):

        user = self.create_user(name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    
    '''GameGear user table'''
    
    class Meta:
        verbose_name_plural = _(u"users")
        verbose_name = _(u"user")
        
    name = models.CharField(max_length=100, unique=True, verbose_name=_(u'user name'))
    email = models.EmailField(max_length=100, unique=True, verbose_name=_(u'email'))
    avatar = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(u'updated at'))
    is_delete = models.BooleanField(default=False, verbose_name=_(u'is deleted'))
    is_active = models.BooleanField(default=True, verbose_name=_(u'is active'))
    #is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, verbose_name=_(u'can login into admin panel'))
    #private info
    nickname = models.CharField(blank=True, max_length=100, verbose_name=_(u'nickname'))
    age = models.IntegerField(blank=False, default=0, verbose_name=_(u'age'))
    job = models.CharField(blank=True, max_length=30, verbose_name=_(u'job'))
    website = models.URLField(blank=True, verbose_name=_(u'web site'))
    interest_in = models.ManyToManyField(InterTag, verbose_name=_(u'interest tag'))
    
    #GameArt
    #posts = models.ManyToManyField(Post, verbose_name=_(u'posts'))
    #own_collections = models.ManyToManyField(Collection, verbose_name=_(u'collections'))
    
    #ref_collections = models.ManyToManyField(Collection, verbose_name=_(u'collections'))
    #pcomments = models.ManyToManyField(PComment, verbose_name=_(u'comments')) 

    reputation = models.IntegerField(blank=False, default=0, verbose_name=_(u'reputation'))   #积分，主题被评分可以获得
    
    #Exchange部分
    e_reputation = models.IntegerField(blank=False,
                                       verbose_name=_(u'e_reputation'),
                                       default=0,)
    #questions
    #anwsers
    
    #token for Oauth
    #weibo_token = models.CharField(verbose_name=u'微博token',max_length=100, blank=True)
    #access_token = models.CharField(max_length=100, blank=True)
    #refresh_token = models.CharField(max_length=100, blank=True)
    #expires_in = models.BigIntegerField(max_length=100, default=0)

    objects = UserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.name

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.name

    

