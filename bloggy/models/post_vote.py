from django.db import models

from bloggy import settings
from bloggy.models.mixin.updatable import Updatable


class Vote(Updatable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_id = models.IntegerField(null=False, help_text='Post id')
    post_type = models.CharField(
        null=False,
        max_length=20,
        choices=settings.get_post_types(),
        help_text="Select content type",
        verbose_name="Content type"
    )

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
