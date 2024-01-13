from django.http import HttpResponseForbidden, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView

from bloggy import settings
from bloggy.models.newsletter import Newsletter


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="newsletter details"), vary_on_cookie], name='dispatch')
class NewsletterDetailsView(TemplateView):
    template_name = "pages/page-newsletter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        newsletter = Newsletter.objects.filter(url=context["url"]).first()
        if newsletter:
            if (newsletter.publish_status == "DRAFT"
                    and not (self.request.user.is_authenticated and self.request.user.is_superuser)):
                raise HttpResponseForbidden("You do not have permission to view this page.")

            context["newsletter"] = newsletter
            return context
        raise Http404
