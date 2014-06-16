#!/usr/bin/env python
#coding:utf-8
#rootdir/rebuild_db.py - rebuild db automatically.
#winkidney 2014 - ver 0.1
import sys,os
from django.core import management


sys.path.append(os.path.realpath(__file__).replace('\\','/'))


if os.path.isfile("gamegear/localsettings.py"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "gamegear.localsettings"
    print 'localsettings'
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = "gamegear.settings"

from UCenter.apis import create_superuser
from GearAnswer.apis import update_node,update_topic,update_reply
from GearAnswer.apis import create_user

def add_default_node():
    update_node('none', 
                'system default node, if your node has no parent node ,set it to this node')
    
def test_info(name, passwd, email):
    user = create_user(name, passwd, email)
    update_topic("游戏齿轮诞生～", 
                 'md', 
                 "游戏齿轮alpha版，由GearDirver强力驱动～～", 
                 'none', 
                 1, 
                 )
    update_reply('md', 
                 '第一条测试回复', 
                 1, 
                 1, 
                 )
    print "Test data added!"
    
    
def syncdb_with_su(su_name, su_email, su_passwd):
    # sync db
    management.call_command('syncdb', interactive=False)
    print "sync done"
    # create super user
    user = create_superuser(su_name, su_passwd, su_email)
    print "super user added"
    

    

if __name__ == '__main__':
    if os.path.isfile('gamegear.db'):
        os.remove('gamegear.db')
    syncdb_with_su('admin', 'admin@admin.com','admin')
    add_default_node()
    test_info('winkidney', '123456', 'kidney@kidney.com')
