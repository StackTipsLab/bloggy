from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView
from django.views.generic import View

from bloggy import settings
from bloggy.models import Post
from bloggy.models.course import Course
from bloggy.models.page import Page
from bloggy.services.post_service import set_seo_settings


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="home"), vary_on_cookie], name='dispatch')
class IndexView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.prefetch_related("category").filter(publish_status="LIVE").order_by(
            "-published_date")[:12]
        context['courses'] = Course.objects.filter(publish_status="LIVE").all()[:6]
        return context


class AdsTextView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(settings.MY_ADS_TXT_CONTENT, content_type='text/plain')


@cache_page(60 * 60 * 24)
def robots(request):
    """
    generates robots.txt, which pretty much does not change
    """
    domain = settings.SITE_URL

    data = f"""User-agent: *
Disallow: /admin/
Disallow: /media/
Disallow: /static/
Disallow: /api/

Sitemap: {domain}/sitemap.xml
"""

    return HttpResponse(data, content_type='text/plain')


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="page"), vary_on_cookie], name='dispatch')
class PageDetailsView(TemplateView):
    template_name = "pages/page-default.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_content = Page.objects.filter(url=context["url"]).first()
        if page_content:
            if (page_content.publish_status == "DRAFT"
                    and not (self.request.user.is_authenticated and self.request.user.is_superuser)):
                raise HttpResponseForbidden("You do not have permission to view this page.")

            context["page"] = page_content
            if page_content.template_type:
                self.template_name = f"pages/page-{page_content.template_type}.html"

            set_seo_settings(post=page_content, context=context)
            return context
        raise Http404
