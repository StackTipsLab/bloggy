from django import forms
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from bloggy.models.page import Page


class PageForm(forms.ModelForm):
    excerpt = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 105}))
    model = Page
    meta_title = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 100}))
    meta_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    meta_keywords = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    prepopulated_fields = {"url": ("title",)}
    list_display = (
        'id',
        'title',
        'url',
    )

    fieldsets = (
        (None, {
            'fields': ('title', 'excerpt', 'url', 'content', 'active',)
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
