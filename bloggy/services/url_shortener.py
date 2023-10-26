
import json
import logging
import os

import requests

logger = logging.getLogger(__name__)


class UrlShortener:
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
    FIREBASE_DYNAMIC_LINKS_DOMAIN = os.getenv('FIREBASE_DYNAMIC_LINKS_DOMAIN')

    def shorten_url(self, original_link):
        response_json = self.firebase_api(original_link)
        logger.debug("Response from Firebase dynamic link", response_json)
        if response_json:
            response = json.loads(response_json)
            return response["shortLink"]

        return original_link

    def firebase_api(self, original_link):
        try:
            url = f"https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={UrlShortener.FIREBASE_API_KEY}"
            headers = {'Content-Type': 'application/json'}
            payload = json.dumps({
                "longDynamicLink": f"{UrlShortener.FIREBASE_DYNAMIC_LINKS_DOMAIN}?link={original_link}"
            })

            response = requests.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                return response.text

        except Exception:
            print("ERROR: while shorting the url")

        return None
