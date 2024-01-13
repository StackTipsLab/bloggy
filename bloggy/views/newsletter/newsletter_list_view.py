from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import ListView
from bloggy import settings
from bloggy.models.newsletter import Newsletter


@method_decorator(
    [cache_page(settings.CACHE_TTL, key_prefix="newsletters"), vary_on_cookie],
    name='dispatch')
class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = "pages/dashboard/newsletters.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletters'] = self.get_recent_feed();
        return context

    def get_recent_feed(self, page=1, page_size=paginate_by):
        newsletters = Newsletter.objects.order_by("-published_date")
        paginator = Paginator(newsletters, page_size)
        try:
            newsletters = paginator.page(page)
        except PageNotAnInteger:
            newsletters = paginator.page(1)
        except EmptyPage:
            newsletters = paginator.page(paginator.num_pages)
        return newsletters
