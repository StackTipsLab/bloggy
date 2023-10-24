import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.views.generic import TemplateView, ListView

from bloggy.models import Article
from bloggy.models import Category

logger = logging.getLogger(__name__)


class TopicsView(TemplateView):
    template_name = "pages/archive/categories.html"

    def get_context_data(self, **kwargs):
        context = super(TopicsView, self).get_context_data(**kwargs)
        categories = Category.objects.filter(article_count__gt=0).order_by("-article_count").all()
        logger.debug('Loading categories: %s', categories)
        context['categories'] = categories

        return context


class TopicsDetailsView(ListView):
    model = Article
    template_name = "pages/archive/articles.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_param = self.kwargs['slug']

        try:
            category = Category.objects.get(slug=category_param)
            context['selected_category'] = category
        except Category.DoesNotExist:
            raise Http404

        articles = Article.objects.filter(category__slug__in=[category_param], publish_status="LIVE").order_by(
            "-published_date")
        paginator = Paginator(articles, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        context['categories'] = Category.objects.filter(article_count__gt=0).order_by("-article_count").all()
        context['seo_title'] = category.title
        context['seo_description'] = category.description
        return context
