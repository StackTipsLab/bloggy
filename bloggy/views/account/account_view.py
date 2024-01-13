from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from bloggy.models import User


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "profile/account_view.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = get_object_or_404(User, username=self.request.user.username)

        # articles = Post.objects.raw('''
        #            select a.id as id, a.title as title, a.slug as slug, a.publish_status as publish_status, a.thumbnail as thumbnail, b.updated_date as bookmark_date from bloggy_article a JOIN bloggy_bookmarks b on a.id=b.post_id  where b.user_id=%s and b.post_type=%s
        #        ''', ([user.id], "article"))

        context.update({
            # 'articles': articles,
            'user': user,
        })
        return context