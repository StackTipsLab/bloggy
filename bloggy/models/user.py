from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

import bloggy
from bloggy import settings
from bloggy.models.mixin.ResizeImageMixin import ResizeImageMixin
from bloggy.services.account_manager import NewUserAccountManager
from bloggy.services.gravtar import get_gravatar
from bloggy.storage_backends import PublicMediaStorage, StaticStorage


def upload_profile_image(self, filename):
    return f'uploads/user/{self.username}/{filename}'


def select_storage():
    return PublicMediaStorage() if settings.USE_SPACES else StaticStorage()


class User(AbstractBaseUser, ResizeImageMixin, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField('email address', unique=True)
    name = models.CharField(_("full name"), max_length=150, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    profile_photo = models.ImageField(null=True, blank=True, upload_to=upload_profile_image,
                                      storage=select_storage)  # , storage=PublicMediaStorage()
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = NewUserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    website = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    youtube = models.CharField(max_length=100, null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "bloggy_user"
        ordering = ['username']
        verbose_name_plural = "Users"

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.username)])

    def get_bookmarks_count(self):
        return bloggy.models.Bookmark.objects.filter(user_id=self.id).count()

    def get_full_name_or_username(self):
        if self.name:
            return self.name
        return self.username

    def __str__(self):
        return self.get_full_name_or_username()

    def get_full_name(self):
        full_name = f"{self.name}"
        return full_name.strip()

    def get_avatar(self):
        if self.profile_photo:
            return self.profile_photo.url
        return get_gravatar(self.email)

    def profile_photo_tag(self):
        if self.profile_photo:
            return format_html(f'<img src="{self.profile_photo.url}" width="auto" height="40"/>')
        return ""
