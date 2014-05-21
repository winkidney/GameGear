# coding:utf-8
# UCenter/forms.py - forms file of the UCenter, for example the UserProfileForm
# by winkidney - ver0.1 - 2014.05.20

from django import forms
from django.utils.translation import ugettext_lazy as _

class UserProfileForm(froms.Form):
    avatar = forms.URLField(required=False)
    username = forms.CharField(max_length=250, required=True)
    decription = forms.CharField(max_length=250, required=False)
    job = forms.CharField(max_length=30, required=False)
    website = forms.URLField(required=False)
    interest_in = forms.CharField(required=False)

def user_info_list(id):
    
    
    [filed_name,field_value]