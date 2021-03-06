#coding:utf-8
#UCenter/apis.py - context processors of the GearAnswer
#ver 0.1 - by winkidney - 2014.05.13
from django.db import models
from UCenter.models import User
from django.core.exceptions import  ObjectDoesNotExist

def create_user(username, password, email):
    
    "Create a User object, return User instance if succeed!"
    
    return User.objects.create_user(username, email, password)


def create_superuser(username, password, email):
    "Create super user by username, passwd, eamil"
    
    return User.objects.create_superuser(username, email, password)
    
def user_exist(username):
    "check if a user exists by its name."
    try:
        User.objects.get(name=username)
        return True
    except:
        return False
    
def get_user_by_id(uid):
    try:
        return User.objects.get(id=uid) 
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
    except ObjectDoesNotExist:
        return False
    
def uid_exist(uid):
    "check if a user exists by its user id."
    try:
        User.objects.get(id=uid)
        return True
    except:
        return False
    
def get_user(request):
    """get a request and return a user obj"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    return authenticate(username=username, password=password)