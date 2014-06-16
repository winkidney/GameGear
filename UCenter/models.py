#!/usr/bin/env python
#coding:utf-8
'''
UCenter.models -- shortdesc
@author:     winkidney
@contact:    winkidney@gmail.com
@deffield    updated: 2014
'''

__all__ = []
__version__ = 0.1
__date__ = '2014-04-14'
__updated__ = '2014-04-14'

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.forms import widgets


from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)

   
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
        
    name = models.CharField(max_length=100, unique=True, verbose_name=_(u'username'))
    email = models.EmailField(max_length=100, unique=True, verbose_name=_(u'email'))
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', verbose_name=_(u'avatar'))
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'create at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(u'updated at'))
    
    is_delete = models.BooleanField(default=False, verbose_name=_(u'is deleted'))
    is_active = models.BooleanField(default=True, verbose_name=_(u'is active'))
    is_staff = models.BooleanField(default=False, verbose_name=_(u'can login into admin panel'))
    
    #private info
    description = models.TextField(blank=True, verbose_name=_(u'self description'))
    good_at = models.CharField(blank=True, max_length=250, verbose_name=_(u'good at'))
    website = models.URLField(blank=True, verbose_name=_(u'website'))
    interests = models.CharField(blank=True, max_length=250, verbose_name=_(u'interests'))

    
    
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
    
    def delete_avatar(self):
        self.avatar.delete()

class Message(models.Model):
    
    """message from a user to another.
       max number for every user is 50.
    """
    
    class Meta:
        verbose_name_plural = _(u"insite message")
        verbose_name = _(u"insite message")
        
    title = models.CharField(max_length=40, verbose_name=_(u'title'))
    message = models.TextField(verbose_name=_(u'message'))
    isread = models.BooleanField(verbose_name=_(u'is read'))
    send_time = models.DateTimeField(auto_now_add=True,verbose_name=_(u'send_time'))
    send_to = models.ForeignKey(User,blank=False, verbose_name=_(u"message's target user"))
    
    def __unicode__(self):
        return "%s" % (self.id, self.send_time)   

