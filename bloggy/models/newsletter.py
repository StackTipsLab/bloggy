from django.db import models
from django.db.models import TextField

from bloggy.models.mixin.updatable import Updatable


class Newsletter(Updatable):
    title = models.CharField(max_length=300, help_text='Enter title')
    url = models.CharField(max_length=150, help_text='Enter url', unique=True)
    content = models.JSONField()
    content_html = TextField(null=True, help_text='Newsletter content')
    published_date = models.DateTimeField(null=True, blank=True)
    publish_status = models.CharField(
        max_length=20,
        choices=[
            ('DRAFT', 'DRAFT'),
            ('LIVE', 'LIVE'),
            ('DELETED', 'DELETED')
        ],
        default='DRAFT', blank=True, null=True,
        help_text="Select publish status",
        verbose_name="Publish status")

    send_to_users_only = models.BooleanField(
        default=False,
        help_text="Send to registered users only"
    )

    send_to_all = models.BooleanField(
        default=False,
        help_text="Send to all users"
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
