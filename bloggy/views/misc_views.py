from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View


class AdsTextView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(settings.MY_ADS_TXT_CONTENT, content_type='text/plain')
