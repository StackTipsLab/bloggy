from django import forms
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from bloggy.models.page import Page


class PageForm(forms.ModelForm):
    excerpt = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 105}))
    url = forms.CharField(widget=forms.URLInput(attrs={'size': 102}))
    meta_title = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'cols': 100}))
    meta_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    meta_keywords = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    model = Page


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    prepopulated_fields = {"url": ("title",)}
    list_display = (
        'id',
        'title',
        'url',
        'excerpt',
        'publish_status',
    )

    fieldsets = (
        (None, {
            'fields': ('title', 'excerpt', 'url', 'content', 'publish_status',)
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
        })
    )

    search_fields = ['title']
    summernote_fields = ('content',)
    readonly_fields = ['updated_date', 'created_date']
    date_hierarchy = 'published_date'
    form = PageForm
    ordering = ('-created_date',)
    list_display_links = ['title']
    list_per_page = 50

    def get_form(self, request, obj=None, change=False, **kwargs):
        return super().get_form(request, obj, change, **kwargs)
