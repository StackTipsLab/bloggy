import uuid

from django.db import models

from bloggy import settings
from bloggy.services.token_generator import TOKEN_LENGTH

TOKEN_TYPE = [
    ('signup', 'signup'),
    ('login', 'login'),
]


def build_repr(instance, fields):
    values = [f"{f}={repr(getattr(instance, f))}" for f in fields]
    return f'{instance.__class__.__name__}({", ".join(values)})'


class VerificationToken(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        db_index=True,
        help_text="A unique identifier for the instance.",
        verbose_name="uuid",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text="The user who owns the email address.",
        on_delete=models.CASCADE,
        related_name="email_addresses",
        related_query_name="email_address",
        verbose_name="user",
    )

    token_type = models.CharField(
        max_length=20,
        choices=TOKEN_TYPE,
        help_text="Token type",
        verbose_name="Token type")

    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text="The time that the token was created.",
        verbose_name="creation time",
    )

    token = models.CharField(
        help_text="The random token identifying the verification request.",
        max_length=TOKEN_LENGTH,
        unique=True,
        verbose_name="token",
    )

    class Meta:
        db_table = "bloggy_verification_token"
        ordering = ("time_created",)
        verbose_name = "verification token"
        verbose_name_plural = "verifications tokens"

    def __repr__(self):
        return build_repr(
            self,
            ["uuid", "time_created", "code"],
        )
