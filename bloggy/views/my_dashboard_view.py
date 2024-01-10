from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from bloggy import settings
from bloggy.models import User


class DashboardView(DetailView):
    template_name = "profile/my_dashboard_view.html"
    DEFAULT_PAGE_SIZE = 12

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.request.user.username)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.get_object()

        posts = user.posts.order_by("-published_date").filter(publish_status="LIVE")
        paginator = Paginator(posts, self.DEFAULT_PAGE_SIZE)
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
