# coding:utf-8
# GearAnswer/forms.py - forms file of the app
# by winkidney - ver0.1 - 2014.05.20
 
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.forms.util import ErrorList
import uuid

from UCenter.apis import create_user
from UCenter.apis import user_exist,email_exist

from GearAnswer.apis import update_avatar,update_node
from GearAnswer.models import EDITOR_TYPES

class CleanErrorList(ErrorList):
    def __unicode__(self):
        if not self:
            return u''
        return u'%s' % ''.join('%s' % e for e in self)
    
def clean_err_form(form_obj, *args, **kwargs):
    return form_obj(*args, error_class=CleanErrorList, **kwargs)

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
        
class NewTopicForm(forms.Form):
    """Because of the auto-tag function,
       the tag field now does not exist.
    """
    title = forms.CharField(required=True, max_length=250)
    editor = forms.ChoiceField(required=True,choices=EDITOR_TYPES)
    content_md = forms.CharField(required=False)
    content_ue = forms.CharField(required=False)
    #tag = forms.CharField(required=False)
    


        
class UserProfileForm(forms.Form):
    avatar = forms.ImageField(required=False)
    #username = forms.CharField(max_length=250, required=True)
    description = forms.CharField(max_length=250, required=False)
    website = forms.URLField(required=False)
    goodat = forms.CharField()
    interests = forms.CharField(required=False)
    
    def save_data(self, user, request):
        #to change , use a api function to do the save job
        image = self.cleaned_data.get('avatar')
        
        if image:
            if user.avatar:
                user.avatar.delete()
            file_ext = image.name.split('.')[1]
            user.avatar.save('%s.%s' % (uuid.uuid1(), file_ext), 
                         image)
        user.description = self.cleaned_data.get('description')
        user.website = self.cleaned_data.get('website')
        user.good_at = self.cleaned_data.get('goodat')
        user.interests = self.cleaned_data.get('interests')
        user.save()
        
class ReplyFrom(forms.Form):
    "You must run check_value method to ensure the data is valid"
    
    reply_to = forms.CharField(required=False, max_length=10)
    editor = forms.ChoiceField(required=True,choices=EDITOR_TYPES)
    comment_md = forms.CharField(required=False)
    comment_ue = forms.CharField(required=False)
    
    def check_value(self):
        if self.cleaned_data.get('comment_%s' \
                                 % self.cleaned_data.get('editor')):
            return True
        return False













