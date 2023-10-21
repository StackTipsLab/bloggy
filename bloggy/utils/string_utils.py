import json

from django.core import serializers


class StringUtils:
    @staticmethod
    def is_blank(text):
        return not (text and text.strip())

    @staticmethod
    def is_not_blank(text):
        return bool(text and text.strip())

    @staticmethod
    def to_json(text):
        tmpJson = serializers.serialize("json", text)
        return json.dumps(json.loads(tmpJson))
