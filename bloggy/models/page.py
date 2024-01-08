from django.db import models
from django.db.models import TextField
from django.urls import reverse

from bloggy.models.mixin.SeoAware import SeoAware
from bloggy.models.mixin.updatable import Updatable


def image_upload_path(self, page_id):
    return f'uploads/pages/{page_id}'


class Page(Updatable, SeoAware):
    """
    Stores page data.
    """

    title = models.CharField(max_length=300, help_text='Enter title')
    template_type = models.CharField(
        max_length=20, choices=[
            ('newsletter', 'Newsletter'),
            ('naked', 'Naked'),
            ('default', 'Default'),
        ],
        default='default', blank=True, null=True,
        help_text="Template type",
        verbose_name="Template type")

    excerpt = models.CharField(
        max_length=500,
        help_text='Enter excerpt',
        null=True,
        blank=True
    )

    url = models.CharField(max_length=150, help_text='Enter url', unique=True)
    thumbnail = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    content = TextField(null=True, help_text='Post content')
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

    def get_admin_url(self):
        return reverse(
            f'admin:{self._meta.app_label}_{self._meta.model_name}_change'
            , args=[self.id])

    def get_admin_url(self):
        return reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=[self.id])

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
