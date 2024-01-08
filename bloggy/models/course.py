from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from hitcount.models import HitCount

from bloggy import settings
from bloggy.models import Category
from bloggy.models.mixin.Content import Content


def upload_thumbnail_image(self, post_id):
    return f'uploads/course/{post_id}'


class Course(Content):
    difficulty = models.CharField(
        max_length=20, choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advance', 'advance'),
        ],
        default='easy', blank=True, null=True,
        help_text="Select difficulty",
        verbose_name="Difficulty level")

    is_featured = models.BooleanField(
        default=False,
        help_text="Should this story be featured on site?"
    )

    description = models.TextField(null=True, help_text='Enter answer')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to=upload_thumbnail_image, null=True, blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name='courses')
    view_count = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ['-display_order']
        verbose_name = "course"
        verbose_name_plural = "courses"
        indexes = [
            models.Index(fields=['slug', 'publish_status', 'published_date']),
        ]

    def get_absolute_url(self):
        return reverse("courses_single", kwargs={"slug": str(self.slug)})

    def get_admin_url(self):
        return reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=[self.id])

    @property
    def get_lessons(self):
        return self.post_set.filter(publish_status="LIVE").order_by("display_order").all()

    def thumbnail_tag(self):
        if self.thumbnail:
            return format_html(f'<img src="{self.thumbnail.url}" width="auto" height="40"/>')
        return ""

    thumbnail_tag.short_description = 'Logo'
    thumbnail_tag.allow_tags = True
