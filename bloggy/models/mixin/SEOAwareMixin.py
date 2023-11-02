from django.db import models


class SEOAwareMixin(models.Model):
    meta_title = models.CharField(max_length=300, help_text='Meta Title', null=True, blank=True)
    meta_description = models.TextField(help_text='Meta Description', null=True, blank=True)
    meta_keywords = models.CharField(max_length=300, help_text='Meta Keywords', null=True, blank=True)

    class Meta:
        abstract = True
