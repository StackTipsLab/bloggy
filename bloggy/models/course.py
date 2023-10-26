from django.contrib.contenttypes.fields import GenericRelation
from django.utils.html import format_html
from django.utils.text import slugify
from django.db import models
from hitcount.models import HitCount

from bloggy import settings
from bloggy.models import Category
from bloggy.models.post import Post
from bloggy.utils.string_utils import StringUtils
from django.urls import reverse


def upload_thumbnail_image(self, post_id):
    return f'uploads/course/{post_id}'


class Course(Post):
    excerpt = models.CharField(max_length=500, help_text='Enter excerpt', null=True, blank=True)

    difficulty = models.CharField(
        max_length=20, choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advance', 'advance'),
        ],
        default='easy', blank=True, null=True,
        help_text="Select difficulty",
        verbose_name="Difficulty level")

    is_featured = models.BooleanField(default=False, help_text="Is featured")
    description = models.TextField(null=True, help_text='Enter answer')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to=upload_thumbnail_image, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    view_count = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ['-display_order']
        verbose_name = "course"
        verbose_name_plural = "courses"
        indexes = [
            models.Index(fields=['slug', 'publish_status', 'published_date']),
        ]

    @staticmethod
    def get_excerpt(self):
        return self.excerpt[0, 10]

    def get_absolute_url(self):
        return reverse("courses_single", kwargs={"slug": str(self.slug)})

    @property
    def get_lessons(self):
        return self.article_set.filter(post_type="lesson").filter(publish_status="LIVE") \
            .order_by("display_order").all()

    def thumbnail_tag(self):
        if self.thumbnail:
            return format_html('<img src="{}" width="auto" height="40"/>'.format(self.thumbnail.url))

    thumbnail_tag.short_description = 'Logo'
    thumbnail_tag.allow_tags = True

    def save(self, *args, **kwargs):
        if StringUtils.is_blank(self.slug):
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
