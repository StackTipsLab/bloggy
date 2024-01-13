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
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sitemaps.views import sitemap, index
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic.base import TemplateView

from bloggy import settings
from bloggy.views import EditProfileView
from bloggy.views.courses_view import CoursesListView, CourseDetailsView, LessonDetailsView
from bloggy.views.page_view import IndexView
from bloggy.views.category_view import CategoriesView, CategoryDetailsView
from .forms.password_reset_form import CustomPasswordResetForm
from .forms.set_password_form import CustomSetPasswordForm
from .services.sitemaps import sitemaps_list
from .views import RegisterView
from bloggy.views.account.account_view import AccountView
from bloggy.views.account.change_password_view import ChangePasswordView
from bloggy.views.newsletter.create_newsletter_view import CreateNewsletterView
from bloggy.views.account.my_dashboard_view import DashboardView
from bloggy.views.newsletter.newsletter_list_view import NewsletterListView
from .views.auth.account_activation_view import AccountActivationView
from .views.newsletter.manage_newsletter_view import ManageNewsletterView
from .views.newsletter.newsletter_details_view import NewsletterDetailsView
from .views.post_view import PostListView, PostDetailsView
from bloggy.views.auth.login_view import MyLoginView
from .views.page_view import AdsTextView, robots
from .views.page_view import PageDetailsView
from .views.quizz_view import QuizListView, QuizDetailView
from .views.rss_view import PostsRssFeed, CoursesRssFeed
from .views.search_view import SearchListView
from bloggy.views.account.update_username_view import UpdateUsernameView
from .views.user_view import PublicProfileView, AuthorsListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/password_change/', PasswordChangeView.as_view(), name='password_change'),

    path('', IndexView.as_view(), name='index'),
    path('articles', PostListView.as_view(), name='posts'),
    path('articles/<slug:slug>', PostDetailsView.as_view(), name='post_single'),

    path('topics', CategoriesView.as_view(), name='categories'),
    path('topics/<str:slug>', CategoryDetailsView.as_view(), name='categories_single'),
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
    path('password-reset/', PasswordResetView.as_view(
        template_name='auth/password_reset.html',
        email_template_name='email/password_reset_email.html',
        form_class=CustomPasswordResetForm
    ), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html',
        form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),

    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('authors', AuthorsListView.as_view(), name="authors"),
    path('user/<str:username>', PublicProfileView.as_view(), name="user_profile"),

    path('account', AccountView.as_view(), name='profile.account'),
    path('edit-profile', EditProfileView.as_view(), name="profile.edit_profile"),
    path('account/update-username', UpdateUsernameView.as_view(), name='profile.account.update_username'),
    path('account/change-password', ChangePasswordView.as_view(), name='profile.account.change_password'),
    path('dashboard', DashboardView.as_view(), name="dashboard"),

    path('newsletter/<path:url>', NewsletterDetailsView.as_view(), name="newsletter.details"),
    path('dashboard/newsletter', NewsletterListView.as_view(), name="dashboard.newsletter"),
    path('dashboard/newsletter/new', CreateNewsletterView.as_view(), name="dashboard.newsletter.new"),
    path('dashboard/newsletter/manage/<str:id>', ManageNewsletterView.as_view(), name="dashboard.newsletter.manage"),

    # path('bookmarks', login_required(UserBookmarksView.as_view()), name="profile.bookmarks"),
    path('contact', TemplateView.as_view(template_name="pages/contact.html"), name='pages.contact'),
    path("rss/articles", PostsRssFeed(), name="articles_feed"),
    path("rss/courses", CoursesRssFeed(), name="courses_feed"),
    path('sitemap.xml', index, {'sitemaps': sitemaps_list}, name='django.contrib.sitemaps.views.index'),
    path('sitemap/<str:section>.xml', sitemap, {'sitemaps': sitemaps_list}, name='django.contrib.sitemaps.views.sitemap'),

    # static files for SEO or other reasons
    path('robots.txt', robots, name='robots'),
    path('ads.txt', AdsTextView.as_view(), name='ads_txt'),

    path('summernote/', include('django_summernote.urls')),
    path('api/1.0/', include('bloggy_api.urls')),

]

if settings.DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()

staticpages = [path('<path:url>', PageDetailsView.as_view()), ]
urlpatterns += staticpages

handler404 = 'bloggy.views.handler_404'
handler500 = 'bloggy.views.handler_500'