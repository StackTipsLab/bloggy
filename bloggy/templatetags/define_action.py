from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from bloggy import settings

register = template.Library()


@register.simple_tag
def define(val=None):
    return val


@register.filter(is_safe=True)
@stringfilter
def expand_media_url(value):
    """Mark the value as a string that should not be auto-escaped."""
    if not settings.DEBUG:
        value = value.replace("\"/media/uploads/", "\"" + settings.ASSETS_DOMAIN + "/media/uploads/")

    return mark_safe(value)
