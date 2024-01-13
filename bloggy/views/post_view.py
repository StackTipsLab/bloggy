from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from bloggy import settings
from bloggy.models import Post, Category
from bloggy.models.course import Course
from bloggy.services.post_service import get_recent_feed, set_seo_settings


@method_decorator(
    [cache_page(settings.CACHE_TTL, key_prefix="posts"), vary_on_cookie],
    name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = "pages/archive/posts.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = get_recent_feed(page=self.request.GET.get('page'))
        context['courses'] = Course.objects.filter(publish_status="LIVE").all()[:2]
        context['categories'] = (Category.objects.filter(article_count__gt=0)
                                 .order_by("-article_count").all())
        return context


@method_decorator(
    [cache_page(settings.CACHE_TTL, key_prefix="post_single"), vary_on_cookie],
    name='dispatch')
class PostDetailsView(HitCountDetailView):
    model = Post
    count_hit = True

    def get_template_names(self):
        if self.object.template_type:
            return f"pages/single/{self.object.post_type}-{self.object.template_type}.html"

        return f"pages/single/{self.object.post_type}.html"

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
                raise HttpResponseForbidden("You do not have permission to view this page.")
            if not (logged_user.username.__eq__(self.object.author.username) or logged_user.is_superuser):
                raise HttpResponseForbidden("You do not have permission to view this page.")

        context = super().get_context_data(**kwargs)
        set_seo_settings(post=self.object, context=context)
        return context
