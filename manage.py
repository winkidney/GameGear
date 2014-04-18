#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.path.isfile("gamegear/localsettings.py"):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamegear.localsettings")
        #print 'localsettings'
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamegear.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
