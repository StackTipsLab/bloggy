from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from bloggy.models.updatable import Updatable
from bloggy.utils.string_utils import StringUtils
from django.utils.html import format_html


def upload_logo_image(self, filename):
    return f'uploads/categories/{filename}'


PUBLISH_STATUS = [
    ('DRAFT', 'DRAFT'),
    ('LIVE', 'LIVE')
]


class Category(Updatable):
    title = models.CharField(max_length=150, help_text='Enter title')
    article_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=150, help_text='Enter slug', unique=True)
    description = models.TextField(max_length=1000, help_text='Enter description', null=True, blank=True)
    logo = models.ImageField(upload_to=upload_logo_image, null=True)
    color = ColorField(default='#1976D2')

    publish_status = models.CharField(
        max_length=20, choices=PUBLISH_STATUS,
        default='DRAFT', blank=True, null=True,
        help_text="Select publish status",
        verbose_name="Publish status")

    class Meta:
        ordering = ['title']
        verbose_name = "category"
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if StringUtils.is_blank(self.slug):
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('categories_single', args=[str(self.slug)])

    def logo_tag(self):
        if self.logo:
            return format_html('<img src="{}" width="auto" height="40"/>'.format(self.logo.url))

    logo_tag.short_description = 'Logo'
    logo_tag.allow_tags = True

    def __str__(self):
        return self.title
