from django import forms
from django.forms import CharField, PasswordInput

from bloggy.models import MyUser


class UpdatePasswordForm(forms.BaseForm):
    model = MyUser

    error_css_class = 'has-error'
    error_messages = {'password_incorrect': "The old password is not correct. Try again."}

    old_password = CharField(
        required=True, label='Password',
        widget=PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'The password can not be empty'})

    new_password1 = CharField(
        required=True, label='Password',
        widget=PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'The password can not be empty'})

    new_password2 = CharField(
        required=True, label='Password (Repeat)',
        widget=PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'The password can not be empty'})
