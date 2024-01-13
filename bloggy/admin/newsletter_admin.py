from django import forms
from django.contrib import admin

from bloggy.admin import BloggyAdmin, publication_fieldsets
from bloggy.models.newsletter import Newsletter


class NewsletterForm(forms.ModelForm):
    model = Newsletter


@admin.register(Newsletter)
class PageAdmin(BloggyAdmin):
    prepopulated_fields = {"url": ("title",)}
    list_display = (
        'id',
        'title',
        'url',
        'publish_status',
    )

    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'content',)
        }), publication_fieldsets)

    search_fields = ['title']
    summernote_fields = ('content',)
    readonly_fields = ['updated_date', 'created_date']
    date_hierarchy = 'published_date'
    form = NewsletterForm
    ordering = ('-created_date',)
    list_display_links = ['title']

    def get_form(self, request, obj=None, change=False, **kwargs):
        return super().get_form(request, obj, change, **kwargs)
