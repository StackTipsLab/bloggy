from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.generic import View


class AdsTextView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(settings.MY_ADS_TXT_CONTENT, content_type='text/plain')


@cache_page(60 * 60 * 24)
def robots(request):
    """
    generates robots.txt, which pretty much does not change
    """
    domain = settings.SITE_URL

    data = """User-agent: *
Disallow: /admin/
Disallow: /media/
Disallow: /static/
Disallow: /api/

Sitemap: {}/sitemap.xml
""".format(domain)

    return HttpResponse(data, content_type='text/plain')
