from django.db import models
from django.db.models import TextField
from bloggy.models.mixin.SEOAwareMixin import SEOAwareMixin
from bloggy.models.mixin.updatable import Updatable


class Page(Updatable, SEOAwareMixin):
    """
    Stores page data.
    """

    title = models.CharField(max_length=300, help_text='Enter title')
    url = models.CharField(max_length=150, help_text='Enter url', unique=True)
    excerpt = models.CharField(
        max_length=500,
        help_text='Enter excerpt',
        null=True,
        blank=True
    )

    content = TextField(null=True, help_text='Post content')
    published_date = models.DateTimeField(null=True, blank=True)
    publish_status = models.CharField(
        max_length=20, choices=[
            ('DRAFT', 'DRAFT'),
            ('LIVE', 'LIVE'),
            ('DELETED', 'DELETED')
        ],
        default='DRAFT', blank=True, null=True,
        help_text="Select publish status",
        verbose_name="Publish status")

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
