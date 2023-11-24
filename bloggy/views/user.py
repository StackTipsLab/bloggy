from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin

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


class PublicProfileView(SingleObjectMixin, View):
    template_name = "pages/user.html"

    def get_object(self, **kwargs):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        if username == 'siteadmin' or username == 'admin' or username == 'superadmin' or username == 'wp-admin':
            raise Http404

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        posts = self.object.posts.filter(publish_status="LIVE").order_by("-published_date")

        paginator = Paginator(posts, DEFAULT_PAGE_SIZE)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['meta_title'] = self.object.get_full_name()
        description = f"{settings.SITE_TITLE} Author. {self.object.get_full_name()}. {self.object.bio}"
        context['meta_description'] = strip_tags(description)
        context['meta_image'] = self.object.get_avatar()

        context.update({
            'posts': posts,
            'user': self.object
        })

        return render(request, self.template_name, context)


class MyProfileView(DetailView):
    # template_name = "pages/user.html"
    template_name = "profile/user_dashboard.html"

    def get_object(self, **kwargs):
        username = self.request.user  # self.kwargs.get("username")
        return get_object_or_404(User, username=username)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.get_object()

        posts = user.posts.order_by("-published_date").filter(publish_status="LIVE")
        paginator = Paginator(posts, DEFAULT_PAGE_SIZE)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context.update({
            'posts': posts,
            'userProfile': user,
            'userType': "self",
        })

        context['meta_title'] = "My Profile"
        context[
            'meta_description'] = f'My profile. Access your {settings.SITE_TITLE} profile, account settings My Profile.'
        if user.profile_photo:
            context['meta_image'] = settings.SITE_LOGO

        return context
