from django.contrib import admin

import bloggy.models.option
from bloggy import settings

admin.site.site_header = settings.SITE_TITLE.upper()
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = "Dashboard"
admin.site.register(bloggy.models.option.Option)

