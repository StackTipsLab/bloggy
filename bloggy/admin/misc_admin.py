from django.contrib import admin
import bloggy.models.option

admin.site.site_header = "STACKTIPS"
admin.site.site_title = "StackTips"
admin.site.index_title = "Dashboard"
admin.site.register(bloggy.models.option.Option)


def publish(model_admin, request, queryset):
    queryset.update(publish_status='LIVE')


publish.short_description = "Publish"


def unpublish(model_admin, request, queryset):
    queryset.update(publish_status='DRAFT')


unpublish.short_description = "Unpublish"
