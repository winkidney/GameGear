#coding:utf-8
#UCenter/apis.py - context processors of the GearAnswer
#ver 0.1 - by winkidney - 2014.05.13
from django.db import models
from UCenter.models import User

def create_user(username, password, email):
    user = User()
    user.name = username
    user.set_password(password)
    user.email = email
    user.save()
    return user

def user_exist(username):
    try:
        User.objects.get(name=username)
        return True
    except:
        return False

def logined(request):
    if request.user.is_authenticated():
            return True
    else:
            return False
        
def email_exist(email):
    try:
        User.objects.get(email=email)
        return True
    except models.Model.DoesNotExist:
        return False
    
def get_user(request):
    """get a request and return a user obj"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    return authenticate(username=username, password=password)