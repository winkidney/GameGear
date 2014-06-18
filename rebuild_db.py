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
from GearAnswer.apis import create_user,create_nav,get_node_byname

def add_default_node():
    update_node('none', 
                'system default node, if your node has no parent node ,set it to this node')
    update_node('创意', 
                '讨论创意有关的话题，新点子？游戏模式？文案？都可以放到这里')
    node = update_node('杂谈', 
                '这里是灌水专用我会乱说么=w=',
                node_avatar=None, pnode='创意',)
    node.help_text = '[>用音乐充实你的创造生活](http://www.xiami.com/radio/play/type/4/oid/5066869)'
    node.save()
    
def test_info(name, passwd, email):
    user = create_user(name, passwd, email)
    update_topic("游戏齿轮诞生～", 
                 'md', 
                 "游戏齿轮alpha版，由GearDirver强力驱动～～", 
                 '杂谈', 
                 1, 
                 )
    update_reply('md', 
                 '第一条测试回复', 
                 1, 
                 1, 
                 )
    print "Test topic added!"
    
def add_nav():    
    node = get_node_byname('杂谈')
    create_nav('创意', 0, node)
    print "Test nav added!"
    
    
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
    add_nav()
