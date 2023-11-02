from django.db import models

from bloggy import settings


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_id = models.IntegerField(null=False, help_text='Post id')
    post_type = models.CharField(
        null=False,
        max_length=20,
        choices=settings.get_post_types(),
        help_text="Select content type",
        verbose_name="Content type"
    )

    created_date = models.DateTimeField(auto_created=True, null=True, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
