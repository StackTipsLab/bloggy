from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView

from bloggy import settings
from bloggy.models import Category, Post
from bloggy.models.course import Course


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="home"), vary_on_cookie], name='dispatch')
class IndexView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Post.objects.prefetch_related("category").filter(publish_status="LIVE").order_by("-published_date")[:12]
        context['courses'] = Course.objects.filter(publish_status="LIVE").all()[:6]
        return context


class AboutPageView(TemplateView):
    template_name = "pages/static/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoryCount'] = Category.objects.filter(article_count__gt=0).order_by("-article_count").count()
        context['postsCount'] = Post.objects.filter(publish_status="LIVE").filter(post_type="article").count()
        context['coursesCount'] = Course.objects.filter(publish_status="LIVE").count()
        return context
