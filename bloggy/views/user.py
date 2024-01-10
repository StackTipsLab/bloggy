from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import DetailView, TemplateView

from bloggy import settings
from bloggy.models import User
from bloggy.services.post_service import DEFAULT_PAGE_SIZE


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="authors"), vary_on_cookie], name='dispatch')
class AuthorsListView(TemplateView):
    template_name = "pages/authors.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = User.objects.filter(is_active=True).filter(is_staff=True).exclude(
            username__in=["siteadmin", "superadmin", "admin"]).all()
        context.update({
            "authors": authors
        })
        return context


class PublicProfileView(DetailView):
    model = User
    template_name = 'pages/user_profile.html'
    context_object_name = 'userProfile'

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        if username == 'siteadmin' or username == 'admin' or username == 'superadmin':
            raise Http404
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object.posts.filter(publish_status="LIVE").order_by("-published_date")
        paginator = Paginator(posts, DEFAULT_PAGE_SIZE)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['meta_title'] = self.object.get_full_name()
        description = f"{settings.SITE_TITLE} Author. {self.object.get_full_name()}. {self.object.bio}"
        context['meta_description'] = strip_tags(description)
        context['meta_image'] = self.object.get_avatar()
        return context
