from django.db import models


class SeoAware(models.Model):
    meta_title = models.CharField(max_length=120, help_text='Meta Title', blank=True, null=True)
    meta_description = models.TextField(help_text='Meta Description', blank=True, null=True)
    meta_keywords = models.CharField(max_length=300, help_text='Meta Keywords', blank=True, null=True)

    class Meta:
        abstract = True
