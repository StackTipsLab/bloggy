import hashlib
import urllib


def get_gravatar(email, size=400):
    default = "identicon"  # "https://media.stacktips.com/media/uploads/default_avatar.png"
    params = urllib.parse.urlencode({'d': default, 's': str(size)})
    return f"https://www.gravatar.com/avatar/{hashlib.md5(email.lower().encode('utf-8')).hexdigest()}?{params}"
