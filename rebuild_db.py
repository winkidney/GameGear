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

from UCenter.models import User
from GearAnswer.apis import update_node

def add_default_node():
    update_node('none', 
                'system default node, if your node has no parent node ,set it to this node')

def syncdb_with_su(su_name, su_email, su_passwd):
    # sync db
    management.call_command('syncdb', interactive=False)
    print "sync done"
    # create super user
    user = User.objects.create_superuser(su_name, su_email, su_passwd)
    #user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.save()
    print "super user added"

if __name__ == '__main__':
    if os.path.isfile('gamegear.db'):
        os.remove('gamegear.db')
    syncdb_with_su('admin', 'admin@admin.com','admin')
    add_default_node()
