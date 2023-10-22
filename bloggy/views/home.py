from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView

from bloggy import settings
from bloggy.models import Category, Article
from bloggy.models.course import Course
from bloggy.services.post_service import get_recent_quizzes
from bloggy.utils.http_utils import HttpUtils


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="home"), vary_on_cookie], name='dispatch')
class IndexView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.prefetch_related("category").filter(publish_status="LIVE").filter(
            post_type__in=["article", "quiz", "lesson"]).order_by("-published_date")[:12]
        context['courses'] = Course.objects.filter(publish_status="LIVE").all()[:6]
        context["quizzes"] = get_recent_quizzes()
        return context


class AboutPageView(TemplateView):
    template_name = "pages/static/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        context['categoryCount'] = Category.objects.filter(article_count__gt=0).order_by("-article_count").count()
        context['postsCount'] = Article.objects.filter(publish_status="LIVE").filter(post_type="article").count()
        context['quizCount'] = Article.objects.filter(publish_status="LIVE").filter(post_type="quiz").count()
        context['coursesCount'] = Course.objects.filter(publish_status="LIVE").count()
        return context
