from django.db import models


class Updatable(models.Model):
    created_date = models.DateTimeField(auto_created=True, null=True, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    def get_model_type(self):
        return self._meta.verbose_name

    class Meta:
        abstract = True
