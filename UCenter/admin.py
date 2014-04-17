#!/usr/bin/env python
#coding:utf-8
# Ucenter/admin.py - by winkidney 2014
#ver : 0.1

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from UCenter.models import Gear
from GameArt.models import Post,Art

class GearInline(admin.StackedInline):
    model = Gear
    can_delete = False
    vervose_name_plural = u"Gear信息"
    
class GearAdmin(UserAdmin):
    inlines = (GearInline,)
    
admin.site.unregister(User)
admin.site.register(User,GearAdmin)
admin.site.register(Gear)
admin.site.register(Post)
admin.site.register(Art)