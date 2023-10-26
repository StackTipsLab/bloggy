from django.db import models
from django.db.models import TextField


class PostMeta(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey('bloggy.Article', on_delete=models.CASCADE)
    meta_key = models.SlugField(max_length=150, help_text='Enter key')
    meta_value = TextField(null=True, help_text='Enter value')

    def __str__(self):
        return f'id:{self.id}, meta_key:{self.meta_key}, meta_value:{self.meta_value}'

    class Meta:
        verbose_name = "Post metadata"
        verbose_name_plural = "Post metadata"
