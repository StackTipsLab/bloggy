from django.conf import settings
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView
from bloggy.models.page import Page


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="page"), vary_on_cookie], name='dispatch')
class PageDetailsView(TemplateView):
    template_name = "pages/page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = context["url"]
        page = Page.objects.filter(url=url).filter(active=True).first()
        if not page:
            raise Http404

        context["page"] = page
        context['meta_title'] = page.meta_title
        context['meta_description'] = page.meta_description
        context['meta_keywords'] = page.meta_keywords
        return context
