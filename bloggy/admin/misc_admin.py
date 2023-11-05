from django.contrib import admin

import bloggy.models.option
from bloggy import settings
from bloggy.models import RedirectRule

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


@admin.register(RedirectRule)
class RedirectRuleAdmin(admin.ModelAdmin):
    list_display = (
        'from_url',
        'to_url',
        'status_code',
        'is_regx',
        'note',
    )
    pass
