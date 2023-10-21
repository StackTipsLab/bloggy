from django.db import models
from bloggy.models.updatable import Updatable


class Post(Updatable):
    display_order = models.IntegerField(null=True, help_text='Display order', default=0)
    title = models.CharField(max_length=300, help_text='Enter title')
    keywords = models.CharField(max_length=300, help_text='Enter title', null=True, blank=True)

    publish_status = models.CharField(
        max_length=20, choices=[
            ('DRAFT', 'DRAFT'),
            ('LIVE', 'LIVE'),
            ('DELETED', 'DELETED')
        ],
        default='DRAFT', blank=True, null=True,
        help_text="Select publish status",
        verbose_name="Publish status")

    published_date = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=150, help_text='Enter slug', unique=True)

    class Meta:
        abstract = True
