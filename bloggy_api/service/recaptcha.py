import json
from urllib import request
from urllib.error import URLError

from bloggy import settings


def recaptcha_verify(recaptcha_response):
    data = {
        'secret': settings.GOOGLE_RECAPTHCA_SECRET_KEY,
        'response': recaptcha_response
    }

    try:
        with request.urlopen(settings.GOOGLE_RECAPTHCA_TOKEN_VERIFY_URL,
                             data=json.dumps(data).encode('utf-8')) as response:
            if response.status == 200:
                result = json.loads(response.read().decode('utf-8'))
                print("Recaptcha verification:", result)
                return True
    except URLError as e:
        print("Recaptcha verification error:", e)
    return False
