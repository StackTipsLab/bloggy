import random
import string

import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

TOKEN_LENGTH = 48


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


def generate_verification_code():
    # Generate a random 20-digit alphanumeric code similar to "JtM8t-MaV8y"
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '-' + ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=10))
    return code.lower()
