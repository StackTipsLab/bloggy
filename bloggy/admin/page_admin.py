from django.contrib import admin

from bloggy.admin import BloggyAdminForm, BloggyAdmin, publication_fieldsets, seo_fieldsets
from bloggy.models.page import Page


class PageForm(BloggyAdminForm):
    model = Page


@admin.register(Page)
class PageAdmin(BloggyAdmin):
    prepopulated_fields = {"url": ("title",)}
    list_display = (
        'id',
        'title',
        'template_type',
        'url',
        'excerpt',
        'publish_status',
    )

    fieldsets = (
        (None, {
            'fields': ('title', 'template_type', 'excerpt', 'url', 'content',)
        }), publication_fieldsets, seo_fieldsets)

    search_fields = ['title']
    summernote_fields = ('content',)
    readonly_fields = ['updated_date', 'created_date']
    date_hierarchy = 'published_date'
    form = PageForm
    ordering = ('-created_date',)
    list_display_links = ['title']

    def get_form(self, request, obj=None, change=False, **kwargs):
        return super().get_form(request, obj, change, **kwargs)
