#coding:utf-8
#GearAnswer/context_processors.py - context processors of the GearAnswer
#ver 0.1 - by winkidney - 2014.05.13
from django.conf import settings
from UCenter.apis import logined
from GearAnswer.apis import get_uinfo

def shared_data(request, *args, **kwagrs):
    data = {'static_url': settings.STATIC_URL,
            'answer_url' : '/',
            #'uinfo_dict': get_uinfo(uid),
            }
    if logined(request):
        data['logined'] = True
        data['cuser'] = request.user
    else:
        data['logined'] = False
    
    
    return data

