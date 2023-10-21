from django.db import models
from bloggy import settings
from bloggy.services import token_generator
from bloggy.services.token_generator import TOKEN_LENGTH


class Subscribers(models.Model):
    email = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=50)
    confirmed = models.BooleanField(null=True, default=False)
    confirmation_code = models.CharField(
        default=None,
        # default=token_generator.generate_verification_code(),
        max_length=TOKEN_LENGTH,
        help_text="The random token identifying the verification request.",
        null=True,
        blank=True,
        verbose_name="token",
    )
    created_date = models.DateTimeField(auto_created=True, null=True, auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user', blank=True,
                             null=True)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"

    class Meta:
        ordering = ['created_date']
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"
