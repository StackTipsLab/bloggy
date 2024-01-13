from django.contrib.auth.decorators import login_required
from django.urls import path

from bloggy_api.views import *
from bloggy_api.views.feedback_api import FeedbackApi

urlpatterns = [
    path('categories', CategoryAPIView.as_view()),
    path('courses', CoursesAPIView.as_view()),

    path('articles', ArticleAPIView.as_view()),
    path('articles/<str:slug>', ArticleDetailsAPIView.as_view()),

    path('users/<str:username>', login_required(UsersAPIView.as_view())),

    path('vote', VoteAPIView.as_view(), name='vote'),
    path('bookmark', BookmarkAPIView.as_view()),

    path('newsletter/subscribe', NewsletterApi.as_view({'post': 'subscribe'})),
    path('newsletter/subscribe', NewsletterApi.as_view({'post': 'subscribe'})),
    path('newsletter/confirm/<int:subscriber_id>/<str:token>', NewsletterApi.as_view({'get': 'confirm'}), name='newsletter_verification'),

    path('comments', CommentsAPIView.as_view()),
    path('comments/<int:id>', CommentsAPIView.as_view()),

    path('quizzes', QuizzesAPIView.as_view()),
    path('quizzes/<int:pk>', QuizDetailsAPIView.as_view()),
    path('feedback', FeedbackApi.as_view({'post': 'feedback'}), name='api.submit_feedback'),
]
