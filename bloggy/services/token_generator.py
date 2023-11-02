import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

TOKEN_LENGTH = 48


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )
