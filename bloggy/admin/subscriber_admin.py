from django.contrib import admin
from django import forms
from django.contrib import admin

from bloggy.models.subscriber import Subscribers


class SubscriberForm(forms.ModelForm):
    model = Subscribers


@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display_links = ['email']
    list_display = ('id', 'email', 'name', 'confirmed', 'created_date')
