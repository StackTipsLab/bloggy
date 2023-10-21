from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from bloggy.models import MyUser, Article


# class UserDashboardView(TemplateView):
#     template_name = "profile/user_dashboard.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(UserDashboardView, self).get_context_data(*args, **kwargs)
#         username = self.request.user.username
#         user = get_object_or_404(MyUser, username=username)
#         context.update({
#             'articles': Article.objects.filter(author_id=user.id).order_by("-published_date").all(),
#             'userProfile': user,
#             'userType': "self",
#         })
#         return context


class UserBookmarksView(TemplateView):
    template_name = "profile/user_bookmarks.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserBookmarksView, self).get_context_data(*args, **kwargs)
        username = self.request.user.username
        user = get_object_or_404(MyUser, username=username)
        # bookmarks = Article.objects.raw(
        #     '''select * from bloggy_article a LEFT JOIN bloggy_bookmarks b on a.`id` = b.`post_id` where b.`user_id` =%s and b.post_type="article"''',
        #     [user.id])

        articles = Article.objects.raw('''
                select a.id as id, a.title as title, a.slug as slug, a.publish_status as publish_status, a.thumbnail as thumbnail, b.updated_date as bookmark_date from bloggy_article a JOIN bloggy_bookmarks b on a.id=b.post_id  where b.user_id=%s and b.post_type=%s
            ''', ([user.id], "article"))

        context.update({
            'articles': articles,
            'userProfile': user,
            'userType': "self",
        })
        return context
