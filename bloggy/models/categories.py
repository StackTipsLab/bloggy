from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify

from bloggy.models.mixin.SeoAware import SeoAware
from bloggy.models.mixin.updatable import Updatable
from bloggy.utils.string_utils import StringUtils


def upload_logo_image(self, filename):
    return f'uploads/categories/{filename}'


class Category(Updatable, SeoAware):
    title = models.CharField(max_length=150, help_text='Enter title')
    article_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=150, help_text='Enter slug', unique=True)
    excerpt = models.TextField(max_length=1000, help_text='Enter description', null=True, blank=True)
    thumbnail = models.ImageField(upload_to=upload_logo_image, null=True)
    color = ColorField(default='#1976D2')

    publish_status = models.CharField(
        max_length=20, choices=[
            ('DRAFT', 'DRAFT'),
            ('LIVE', 'LIVE')
        ],
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
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('categories_single', args=[str(self.slug)])

    def thumbnail_tag(self):
        if self.thumbnail_tag:
            return format_html(f'<img src="{self.thumbnail.url}" width="auto" height="40"/>')
        return ""

    thumbnail_tag.short_description = 'Thumbnail'
    thumbnail_tag.allow_tags = True

    def __str__(self):
        return str(self.title)
