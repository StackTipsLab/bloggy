from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from bloggy import settings
from bloggy.models import MyUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bloggy.services.post_service import DEFAULT_PAGE_SIZE


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="authors"), vary_on_cookie], name='dispatch')
class AuthorsListView(TemplateView):
    template_name = "pages/authors.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = MyUser.objects.filter(is_active=True).filter(is_staff=True).exclude(
            username__in=["siteadmin", "superadmin", "admin"]).all()
        context.update({
            "authors": authors
        })
        return context


class PublicProfileView(SingleObjectMixin, View):
    template_name = "pages/user.html"

    def get_object(self, **kwargs):
        username = self.kwargs.get("username")
        return get_object_or_404(MyUser, username=username)

    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        if username == "nilanchala":
            return redirect(reverse('user_profile', kwargs={'username': "nilan"}))

        if username == 'siteadmin' or username == 'admin' or username == 'superadmin' or username == 'wp-admin':
            raise Http404

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # user = get_object_or_404(MyUser.objects.filter(is_active=True), username=username)
        articles = self.object.articles.filter(publish_status="LIVE").order_by("-published_date")

        paginator = Paginator(articles, DEFAULT_PAGE_SIZE)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context['seo_title'] = self.object.get_full_name()
        description = "StackTips Author. {}. {}".format(self.object.get_full_name(), self.object.bio)
        context['seo_description'] = strip_tags(description)
        context['seo_image'] = self.object.get_avatar()

        context.update({
            'articles': articles,
            'userProfile': self.object
        })

        return render(request, self.template_name, context)


class MyProfileView(DetailView):
    # template_name = "pages/user.html"
    template_name = "profile/user_dashboard.html"

    def get_object(self, **kwargs):
        username = self.request.user  # self.kwargs.get("username")
        return get_object_or_404(MyUser, username=username)

    def get_context_data(self, *args, **kwargs):
        context = super(MyProfileView, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        logged_user = self.request.user

        articles = user.articles.order_by("-published_date").filter(publish_status="LIVE")
        paginator = Paginator(articles, DEFAULT_PAGE_SIZE)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context.update({
            'articles': articles,
            'userProfile': user,
            'userType': "self",
        })

        context['seo_title'] = "My Profile"
        context['seo_description'] = "My profile. Access your profile, account settings My Profile. You need a StackTips account to sign in and view your profile."
        if user.profile_photo:
            context['seo_image'] = "https://media.stacktips.com/static/media/logo.png"

        return context

# def add_follow(self, request):
#     user = self.get_object()
#     user.profile.followed_by.add(request.user.profile)
# def get_context_data(self, *args, **kwargs):
#     # //username = self.kwargs.get("username")
#
#
#     # user = User.all().fi
#
#     profile = get_object_or_404(Profile, user_id=self.request.user.id)
#     print(profile)
#     context['profile'] = profile
#     return context
#
# # def get_context_data(self, *args, **kwargs):
# #     context = super(Profile, self).get_context_data(*args, **kwargs)
# #     user = self.get_object()
# #     context.update({
# #         'startups': user.startups.all()  # .filter(created_date__lte=timezone.now()).order_by(' -created_date')
# #     })
# #     return context
#
# # def get_context_data(self, request, **kwargs):
# #     user_form = UserForm(request.user)
# #     profile_form = ProfileForm(request.user.profile)
# #     context['user'] = request.user
# #     context['user_form'] = user_form
# #     context['profile_form'] = profile_form
# #     return context
