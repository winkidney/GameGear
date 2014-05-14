#coding:utf-8
#GearAnswer/context_processors.py - context processors of the GearAnswer
#ver 0.1 - by winkidney - 2014.05.13
from django.conf import settings

def shared_data(request, *args, **kwagrs):
    data = {'static_url': settings.STATIC_URL,
            }
    return data