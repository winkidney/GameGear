# coding:utf-8
# GearAnswer/forms.py - forms file of the app
# by winkidney - ver0.1 - 2014.05.20
 
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from UCenter.apis import create_user
from UCenter.apis import user_exist,email_exist

class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True)
    password = forms.CharField(max_length=20, required=True)
    


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=250,required=True)
    password1 = forms.CharField(max_length=20, required=True)
    password2 = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    
    def check_value(self):
        # Check that the two password entries match
        if user_exist(self.cleaned_data.get("username")):
            self.errors['username'] = _(u'Username existed!')
            return False
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.errors['password2'] = _(u'Tow password inputs are different!')
            return False
        if email_exist(self.cleaned_data.get("email")):
            self.errors['email'] = _(u'Email existed!')
            return False
        return True
        
        
    
    def save_user(self):
        # Save the provided password in hashed format
        create_user(self.cleaned_data.get('username'),
                    self.cleaned_data["password1"],
                    self.cleaned_data.get('email')
                    )
