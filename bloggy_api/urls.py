from django.contrib.auth.decorators import login_required
from django.urls import path

from bloggy_api.views.articles_api import ArticleAPIView, ArticleDetailsAPIView
from bloggy_api.views.bookmark_api import BookmarkAPIView
from bloggy_api.views.category_api import CategoryAPIView
from bloggy_api.views.comments_api_view import CommentsAPIView
from bloggy_api.views.course_api import CoursesAPIView
from bloggy_api.views.newsletter_api import NewsletterApi
from bloggy_api.views.user_api import UsersAPIView
from bloggy_api.views.vote_api import VoteAPIView

urlpatterns = [
    path('categories', CategoryAPIView.as_view()),
    path('courses', CoursesAPIView.as_view()),
    path('articles', ArticleAPIView.as_view()),
    path('articles/<str:slug>', ArticleDetailsAPIView.as_view()),
    path('users/<str:username>', login_required(UsersAPIView.as_view())),
    path('vote', VoteAPIView.as_view(), name='vote'),
    path('bookmark', BookmarkAPIView.as_view()),
    path('newsletter/subscribe', NewsletterApi.as_view({'post': 'subscribe'})),
    path('newsletter/confirm/<int:subscriber_id>/<str:token>', NewsletterApi.as_view({'get': 'confirm'}),
         name='newsletter_verification'),
    path('comments', CommentsAPIView.as_view()),
    path('comments/<int:id>', CommentsAPIView.as_view()),
]
