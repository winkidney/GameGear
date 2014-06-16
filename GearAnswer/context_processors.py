#coding:utf-8
#GearAnswer/context_processors.py - context processors of the GearAnswer
#ver 0.1 - by winkidney - 2014.05.13
from django.conf import settings
from UCenter.apis import logined
from GearAnswer.apis import get_uinfo

def shared_data(request, *args, **kwagrs):
    data = {'static_url': settings.STATIC_URL,
            'answer_url' : '/',
            'current_user': get_uinfo(request.user.id),
            'site_name'  : 'GameGear',
            'md_help' : 'http://wiki.gg-workshop.com/doku.php?id=%E6%96%87%E6%A1%A3:%E4%BD%BF%E7%94%A8markdown%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98',
            'none' : '',
            
            'guide_url' : 'http://wiki.gg-workshop.com/doku.php?id=%E6%96%87%E6%A1%A3:%E7%A4%BE%E5%8C%BA%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97',
            'art_url' : 'http://wiki.gg-workshop.com/doku.php?id=%E4%BC%81%E5%88%92:gamegear:gearart',
            'projects_url' : 'http://wiki.gg-workshop.com/doku.php?id=%E4%BC%81%E5%88%92:gamegear:gearprojects',
            }
    if logined(request):
        data['logined'] = True
        data['cuser'] = request.user
    else:
        data['logined'] = False
    
    
    return data

