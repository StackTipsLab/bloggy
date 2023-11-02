import random
import string
from datetime import timedelta

from django.utils.timezone import now

from bloggy.models import VerificationToken

TOKEN_VALIDITY = 30


def create_token(user, token_type):
    """
    Generate token:: Token and uuid will be generated automatically
    """
    token = VerificationToken.objects.filter(user=user, token_type=token_type).first()
    if token:
        time_difference = now() - token.time_created
        time_difference_in_minutes = time_difference / timedelta(minutes=1)

        # return the existing token, if it is not expired
        if time_difference_in_minutes < TOKEN_VALIDITY:
            return token

        token.delete()

    return VerificationToken.objects.create(user=user, token_type=token_type, token=generate_verification_code())


def get_token(uuid, verification_token, token_type):
    return VerificationToken.objects \
        .filter(uuid__exact=uuid, token=verification_token, token_type=token_type) \
        .first()


def is_token_expired(token):
    if not token:
        return True

    time_difference = now() - token.time_created
    time_difference_in_minutes = time_difference / timedelta(minutes=1)
    if time_difference_in_minutes > TOKEN_VALIDITY:
        return True

    return False


def delete_token_by_uuid(uuid):
    return VerificationToken.objects.filter(uuid=uuid).delete()


def generate_verification_code():
    # Generate a random 20-digit alphanumeric code similar to "JtM8t-MaV8y"
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '-' + ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=10))
    return code.lower()
