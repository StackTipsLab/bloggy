from django.db import models
from django.db.models import TextField

from bloggy.models.updatable import Updatable


class Option(Updatable):
    id = models.AutoField(primary_key=True)
    key = models.SlugField(max_length=150, help_text='Enter key', unique=True)
    value = TextField(null=True, help_text='Enter value')

    def __str__(self):
        return str(self.key)
