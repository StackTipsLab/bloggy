import json
import urllib
# from urllib.request import urlopen

from bloggy import settings


class HttpUtils:

    @staticmethod
    def read_file(file_path):
        try:
            print(""
                  "Fetching data from {}", settings.ASSETS_DOMAIN+file_path)
            request = urllib.request.Request(settings.ASSETS_DOMAIN + file_path, method="GET")
            response = urllib.request.urlopen(request)
            return json.load(response)
        except Exception as e:
            print("Error fetching data from {}: {}", file_path, e)
        return None

    pass
