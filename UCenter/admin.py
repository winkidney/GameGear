#!/usr/bin/env python
#coding:utf-8
# Ucenter/admin.py - by winkidney 2014
#ver : 0.1

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from UCenter.models import (User, Message)

# 新增用户表单
class UserCreateForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('name', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# 修改用户表单
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_(u"Password"),
        help_text=_(u"Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>.")
                                         )

    class Meta:
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
    
    
class GearAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreateForm

    list_display = ('name', 'created_at', 'email', 'is_delete', 'is_staff')
    search_fields = ('name', 'email')
    list_filter = ('is_staff',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'avatar',)}),
        (_(u'Personal info'), {'fields': ('created_at', 'updated_at', 'description', 'good_at' , 'website', 'interests')}),
        #(_(u'GearArt'),{'fields' : ('reputation',)}),
        #(_(u'GearAnswer'),{'fields' : ('a_reputation',)}),
        
        #(
        #    'Open token info',
        #    {
        #        'fields': ('access_token', 'refresh_token', 'expires_in')
        #    }
        #),
        (_(u'Permissions'), {'fields': ('is_delete', 'is_staff', 
                                        'is_active', 'is_superuser',
                                        'user_permissions',
                                        'groups',)}),
        (_(u'Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('name', 'email', 'password1', 'password2'),
            }
        ),
    )
    ordering = ('created_at',)
    filter_horizontal = ('groups', 'user_permissions',)

    

admin.site.register(User, GearAdmin)
admin.site.register(Permission)
admin.site.unregister(DjangoGroup)
admin.site.register(Message)
