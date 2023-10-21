from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from bloggy import settings
from bloggy.models import Article, Category
from bloggy.models.course import Course
from bloggy.services.post_service import get_recent_feed


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="articles"), vary_on_cookie], name='dispatch')
class ArticleListView(ListView):
    model = Article
    template_name = "pages/archive/articles.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['articles'] = get_recent_feed(page=self.request.GET.get('page'))
        context['courses'] = Course.objects.filter(publish_status="LIVE").all()[:2]
        context['categories'] = Category.objects.filter(article_count__gt=0).order_by("-article_count").all()
        return context


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="article_single"), vary_on_cookie], name='dispatch')
class ArticleDetailsView(HitCountDetailView):
    model = Article
    count_hit = True

    def get_template_names(self):
        post_meta = self.object.get_postmeta()
        if post_meta is not None and 'template_type' in post_meta:
            return "pages/single/{}-{}.html".format(self.object.post_type, post_meta['template_type'])
        else:
            return "pages/single/{}.html".format(self.object.post_type)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):

        # check if article is published? if live no issues.
        if self.object.publish_status == "DRAFT":
            logged_user = self.request.user

            # If not live, check for the context parameter and the user login status
            # If user is the owner of the post or user is an admin, can preview the post
            if not logged_user:
                raise HttpResponse('Unauthorized', status=401)
            if not (logged_user.username.__eq__(self.object.author.username) or logged_user.is_superuser):
                raise HttpResponse('Unauthorized', status=401)

        context = super().get_context_data(**kwargs)
        context["seo_title"] = self.object.title
        context["seo_description"] = self.object.excerpt
        context['seo_keywords'] = self.object.keywords

        if self.object.thumbnail:
            context['seo_image'] = self.object.thumbnail.url
            context['og_image'] = self.object.thumbnail.url
        else:
            context['og_image'] = "{}/media/opengraph/{}/{}.png".format(settings.ASSETS_DOMAIN, self.object.post_type,
                                                                        self.object.slug)
        return context
