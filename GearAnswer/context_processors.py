#coding:utf-8
#GearAnswer/context_processors.py - context processors of the GearAnswer
#ver 0.1 - by winkidney - 2014.05.13
from django.conf import settings
from GearAnswer.apis import logined

def shared_data(request, *args, **kwagrs):
    data = {'static_url': settings.STATIC_URL,
            'answer_url' : '/',
            }
    if logined(request):
        data['logined'] = True
    else:
        data['logined'] = False
        
    
    return data

