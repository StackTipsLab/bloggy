from django.contrib import sitemaps
from django.contrib.sitemaps import GenericSitemap
from django.urls import reverse
from bloggy.models import Post, Category, User
from bloggy.models.course import Course
from bloggy.models.page import Page


class StaticPagesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        items = []
        staticPages = [
            'index',
            'courses',
            'posts',
            'categories',
            'authors']

        for staticPage in staticPages:
            items.append(reverse(staticPage))

        pages = Page.objects.filter(publish_status="LIVE").all()
        for page in pages:
            items.append(f'/{page.url}')
        return items

    def location(self, item):
        return item


sitemaps_list = {
    'pages': StaticPagesSitemap,
    'articles': GenericSitemap({
        'queryset': Post.objects.filter(publish_status="LIVE").order_by("-published_date").all(),
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
        'queryset': User.objects.exclude(username__in=["siteadmin", "superadmin", "admin"]).filter(is_staff=True).all()
    }, priority=0.6, changefreq='daily'),

}
