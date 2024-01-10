import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.views.generic import TemplateView, ListView

from bloggy import settings
from bloggy.models import Category, Course
from bloggy.models import Post
from bloggy.services.post_service import set_seo_settings

logger = logging.getLogger(__name__)


class CategoriesView(TemplateView):
    template_name = "pages/archive/categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if settings.SHOW_EMTPY_CATEGORIES:
            categories = Category.objects.order_by("-article_count").all()
        else:
            categories = Category.objects.filter(article_count__gt=0).order_by("-article_count").all()

        context['categories'] = categories
        return context


class CategoryDetailsView(ListView):
    model = Post
    template_name = "pages/archive/posts.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_param = self.kwargs['slug']

        try:
            category = Category.objects.get(slug=category_param)
            context['selected_category'] = category
        except Category.DoesNotExist:
            raise Http404

        posts = Post.objects.filter(category__slug__in=[category_param], publish_status="LIVE").order_by(
            "-published_date")

        courses = Course.objects.filter(category=category, publish_status="LIVE").order_by(
            "-published_date")

        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['courses'] = courses
        context['categories'] = Category.objects.filter(article_count__gt=0).order_by("-article_count").all()

        set_seo_settings(post=category, context=context)
        return context
