from django.db import models
from django.utils.text import slugify
from bloggy.models.mixin.SeoAware import SeoAware
from bloggy.models.mixin.updatable import Updatable
from bloggy.utils.string_utils import StringUtils


class Content(Updatable, SeoAware):
    title = models.CharField(max_length=300, help_text='Enter title')
    slug = models.SlugField(max_length=150, help_text='Enter slug', unique=True)
    excerpt = models.CharField(
        max_length=500,
        help_text='Enter excerpt',
        null=True,
        blank=True
    )

    display_order = models.IntegerField(null=True, help_text='Display order', default=0)
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

    def get_excerpt(self):
        return self.excerpt[:10]

    def save(self, *args, **kwargs):
        if StringUtils.is_blank(self.slug):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    class Meta:
        abstract = True
