from django.db import models

from bloggy import settings


class Bookmarks(models.Model):
    CONTENT_TYPES = [
        ('question', 'question'),
        ('article', 'article'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_id = models.IntegerField(null=False, help_text='Post id')
    post_type = models.CharField(null=False, max_length=20, choices=CONTENT_TYPES,
                                 help_text="Select content type", verbose_name="Content type")

    created_date = models.DateTimeField(auto_created=True, null=True, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
