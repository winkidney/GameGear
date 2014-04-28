#!/usr/bin/env python
#coding:utf-8
# Ucenter/admin.py - by winkidney 2014
#ver : 0.1

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import (Node, Tag, Answer, Question, Nav, Setting)


admin.site.register(Node)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Nav)
admin.site.register(Setting)

