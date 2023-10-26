from django.contrib import sitemaps
from django.contrib.sitemaps import GenericSitemap
from django.urls import reverse

from bloggy.models.course import Course
from bloggy.models import Article, Category, MyUser


class StaticPagesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'index',
            'courses',
            'quizzes',
            'articles',
            'categories',
            'authors',
            'pages.privacy',
            'pages.code_of_conduct',
            'pages.contribute',
            'pages.about',
            'pages.contact',
            'pages.terms_of_service',
            'pages.cookie_policy',
            'resources',
            'resources.status_codes',
            'resources.base64_converter',
            'resources.url_encoder',
            'resources.analyze_http_header',
            'resources.website_link_analyzer',
        ]

    def location(self, item):
        if item.startswith("/"):
            return item

        return reverse(item)


sitemaps_list = {
    'pages': StaticPagesSitemap,
    'articles': GenericSitemap({
        'queryset': Article.objects.filter(publish_status="LIVE").order_by("-published_date").all(),
        'date_field': 'published_date'
    }, priority=0.6, changefreq='daily'),

    'courses': GenericSitemap({
        'queryset': Course.objects.filter(publish_status="LIVE").order_by("-published_date").all(),
        'date_field': 'published_date'
    }, priority=0.6, changefreq='daily'),

    'categories': GenericSitemap({
        'queryset': Category.objects.filter(publish_status="LIVE").all(), 'date_field': 'updated_date'
    }, priority=0.6, changefreq='daily'),

    'users': GenericSitemap({
        'queryset': MyUser.objects.exclude(username__in=["siteadmin", "superadmin", "admin"]).filter(is_staff=True).all()
    }, priority=0.6, changefreq='daily'),

}
