from django.contrib import admin

import bloggy.models.option
from bloggy import settings

admin.site.site_header = settings.SITE_TITLE.upper()
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = "Dashboard"
admin.site.register(bloggy.models.option.Option)


def publish(model_admin, request, queryset):
    queryset.update(publish_status='LIVE')


publish.short_description = "Publish"


def unpublish(model_admin, request, queryset):
    queryset.update(publish_status='DRAFT')


unpublish.short_description = "Unpublish"
