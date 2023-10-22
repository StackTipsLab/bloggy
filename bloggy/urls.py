"""bloggy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap, index
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic.base import TemplateView

from bloggy import settings
from bloggy.views import EditProfileView
from bloggy.views.courses_view import CoursesListView, CourseDetailsView, LessonDetailsView
from bloggy.views.home import IndexView, AboutPageView
from bloggy.views.topics_view import CategoriesView, CategoriesDetailsView
from .services.sitemaps import sitemaps_list
from .views import RegisterView
from .views.account import AccountActivationView
from .views.article_views import ArticleListView, ArticleDetailsView
from .views.login import MyLoginView
from .views.misc_views import AdsTextView
from .views.old_blog_redirect_view import AuthorRedirectView
from .views.old_blog_redirect_view import OldCategoryDetailsRedirectView
from .views.old_blog_redirect_view import OldTagArchiveRedirectView
from .views.quizzes_view import QuizListView, QuizDetailView
from .views.rss import ArticlesRssFeed, CoursesRssFeed
from .views.search_view import SearchListView

from .views.user import MyProfileView, PublicProfileView, AuthorsListView
from .views.user_collections import UserBookmarksView
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/password_change/', PasswordChangeView.as_view(), name='password_change'),

    path('', IndexView.as_view(), name='index'),
    path('articles', ArticleListView.as_view(), name='articles'),
    path('articles/<slug:slug>', ArticleDetailsView.as_view(), name='article_single'),
    path('topics', CategoriesView.as_view(), name='categories'),
    path('topics/<str:slug>', CategoriesDetailsView.as_view(), name='categories_single'),
    path('search', SearchListView.as_view(), name='search'),
    path('courses', CoursesListView.as_view(), name='courses'),
    path('courses/<slug:slug>', CourseDetailsView.as_view(), name='courses_single'),
    path('courses/<str:course>/<slug:slug>', LessonDetailsView.as_view(), name='lesson_single'),
    path('quizzes', QuizListView.as_view(), name='quizzes'),
    path('quizzes/<slug:slug>', QuizDetailView.as_view(), name='quiz_single'),

    path('login', MyLoginView.as_view(template_name="auth/login.html"), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('activate/<str:uuid>/<str:token>', AccountActivationView.as_view(), name='activate_account'),
    path('authors', AuthorsListView.as_view(), name="authors"),
    path('user/<str:username>', PublicProfileView.as_view(), name="user_profile"),

    path('edit-profile', login_required(EditProfileView.as_view()), name="profile.edit_profile"),
    path('dashboard', login_required(MyProfileView.as_view()), name="profile.dashboard"),
    path('bookmarks', login_required(UserBookmarksView.as_view()), name="profile.bookmarks"),

    path('privacy', TemplateView.as_view(template_name="pages/static/privacy-policy.html"), name='pages.privacy'),
    path('code-of-conduct', TemplateView.as_view(template_name="pages/static/code_of_conduct.html"),
         name='pages.code_of_conduct'),
    path('contribute', TemplateView.as_view(template_name="pages/static/contribute.html"), name='pages.contribute'),
    path('about', AboutPageView.as_view(), name='pages.about'),
    path('contact', TemplateView.as_view(template_name="pages/static/contact.html"), name='pages.contact'),
    path('terms-of-service', TemplateView.as_view(template_name="pages/static/terms-of-service.html"),
         name='pages.terms_of_service'),
    path('cookie-policy', TemplateView.as_view(template_name="pages/static/cookie-policy.html"),
         name='pages.cookie_policy'),

    path("rss/articles", ArticlesRssFeed(), name="articles_feed"),
    path("rss/courses", CoursesRssFeed(), name="courses_feed"),
    path('sitemap.xml', index, {'sitemaps': sitemaps_list}, name='django.contrib.sitemaps.views.index'),
    path('sitemap/<str:section>.xml', sitemap, {'sitemaps': sitemaps_list},
         name='django.contrib.sitemaps.views.sitemap'),

    # static files for SEO or other reasons
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('ads.txt', AdsTextView.as_view(), name='ads_txt'),
    path('220764bdee4b4ff297c588217aaaafa3.txt',
         TemplateView.as_view(template_name="220764bdee4b4ff297c588217aaaafa3.txt", content_type="text/plain")),

    # redirects for old website migration
    path('author/<str:user>', AuthorRedirectView.as_view()),
    path('tag/<str:tagname>', OldTagArchiveRedirectView.as_view()),
    path('topics/tutorials/<str:category>', OldCategoryDetailsRedirectView.as_view()),
    # END redirections

    path('summernote/', include('django_summernote.urls')),
    path('api/1.0/', include('bloggy_api.urls')),
]

if settings.DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()

handler404 = 'bloggy.views.handler_404'
handler500 = 'bloggy.views.handler_500'
