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
from django.db import models


from GearArt.models import Collection,Post,PComment

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)

class Message(models.Model):
    
    """message from a user to another.
       max number for every user is 50.
    """
    
    message = models.TextField(verbose_name=_(u'message'))
    isread = models.BooleanField(verbose_name=u'isread')
    send_time = models.DateTimeField(auto_now_add=True,verbose_name=_(u'send_time'))

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

    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    avatar = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'用户创建时间')
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    #private info
    nickname = models.CharField(blank=True, max_length=100)
    age = models.IntegerField(blank=False, default=0)
    job = models.CharField(blank=True, max_length=30)
    website = models.URLField(blank=True)
    
    
    #GameArt
    posts = models.ManyToManyField(Post, verbose_name=_(u'posts'))
    own_collections = models.ManyToManyField(Collection, verbose_name=_(u'collections'))
    
    #ref_collections = models.ManyToManyField(Collection, verbose_name=_(u'collections'))
    pcomments = models.ManyToManyField(PComment, verbose_name=_(u'comments')) 

    reputation = models.IntegerField(blank=False,default=0)   #积分，主题被评分可以获得
    
    #Exchange部分
    e_reputation = models.IntegerField(blank=False,
                                       verbose_name=u'E_reputation',
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

    

