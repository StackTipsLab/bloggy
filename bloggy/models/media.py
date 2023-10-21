from django.db import models
from django_summernote.models import AbstractAttachment
from django_summernote.utils import get_config


class Media(AbstractAttachment):
    post_id = models.TextField(max_length=300, help_text='Enter post ID', null=True, blank=True)
    post_type = models.CharField(
        max_length=20, choices=[
            ('article', 'article'),
            ('question', 'question'),
            ('category', 'category'),
        ], default='article', blank=True, null=True, help_text="Select post type", verbose_name="Post type")
    media_type = models.CharField(max_length=255, null=True, blank=True,
                                  help_text="Media type like attachment, thumbnail")

    def save(self, *args, **kwargs):
        get_config()['attachment_upload_to'] = f'uploads/{self.post_type}/{self.post_id}'
        super(Media, self).save(*args, **kwargs)

    def get_attachment_upload_to(self):
        return f'uploads/{self.post_type}/{self.post_id}'
