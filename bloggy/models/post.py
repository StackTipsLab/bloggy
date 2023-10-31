from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import TextField
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from hitcount.models import HitCount

import bloggy
from bloggy import settings
from bloggy.models import Category, Vote, Bookmark
from bloggy.models.course import Course
from bloggy.models.mixin.Content import Content
from bloggy.utils.string_utils import StringUtils


def upload_thumbnail_image(post_id):
    return f'uploads/articles/{post_id}'


class Post(Content):
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

    video_id = models.CharField(
        max_length=100,
        help_text='YouTube Video ID',
        null=True,
        blank=True
    )

    post_type = models.CharField(
        max_length=20, choices=settings.get_post_types(),
        default='article', blank=True, null=True,
        help_text="Post type",
        verbose_name="Post type")

    template_type = models.CharField(
        max_length=20, choices=[
            ('standard', 'Standard'),
            ('cover', 'Cover'),
            ('naked', 'Naked'),
            ('full', 'Full'),
        ],
        default='standard', blank=True, null=True,
        help_text="Template type",
        verbose_name="Template type")

    content = TextField(null=True, help_text='Post content')
    thumbnail = models.ImageField(upload_to=upload_thumbnail_image, blank=True, null=True)

    # This comes from Django HitCount
    view_count = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    category = models.ManyToManyField(Category)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = "article"
        verbose_name_plural = "articles"
        indexes = [
            models.Index(fields=['slug', 'publish_status', 'post_type', 'published_date']),
        ]

    def get_comments_count(self):
        return bloggy.models.Comment.objects.filter(post_id=self.id).count()

    def get_admin_url(self):
        return reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=[self.id])

    def get_absolute_url(self):
        if self.post_type == "lesson":
            return reverse("lesson_single", kwargs={"course": str(self.course.slug), "slug": str(self.slug)})
        else:
            return reverse("article_single", kwargs={"slug": str(self.slug)})

    @property
    def get_votes_count(self):
        return Vote.objects.all().filter(post_id=self.id).filter(post_type="article").count()

    @property
    def get_read_count(self):
        words_per_minute = 150
        word_count = round(len(self.content.split()) / words_per_minute)
        return str(max(word_count, 5)) + " minutes"

    def get_bookmarks_count(self):
        return Bookmark.objects.all().filter(post_id=self.id).count()

    def thumbnail_tag(self):
        if self.thumbnail:
            return format_html(f'<img src="{self.thumbnail.url}" width="auto" height="40"/>')
        return ''

    thumbnail_tag.short_description = 'Logo'
    thumbnail_tag.allow_tags = True

    def save(self, *args, **kwargs):
        if StringUtils.is_blank(self.slug):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_template_path(self):
        return f"pages/{self.post_type}-{self.template_type}.html"
