from datetime import date

from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from bloggy import settings
from bloggy.models import Article
from bloggy.models.course import Course


class ImageRssFeedGenerator(feedgenerator.Rss201rev2Feed):
    def add_root_elements(self, handler):
        super(ImageRssFeedGenerator, self).add_root_elements(handler)
        handler.startElement('image', {})
        handler.addQuickElement("url", self.feed['logo'])
        handler.addQuickElement("title", self.feed['title'])
        handler.addQuickElement("link", self.feed['link'])
        handler.endElement('image')


class BaseRssFeedView(Feed):
    feed_type = ImageRssFeedGenerator
    content_type = 'application/xml; charset=utf-8'
    description = "most recent 30 from stacktips.com"
    language = "en"

    def feed_extra_kwargs(self, obj):
        return {
            'logo': settings.SITE_LOGO,
            'icon': 'https://media.stacktips.com/static/media/favicon/favicon-32x32.png'
        }

    def item_title(self, obj):
        return obj.title

    def item_link(self, obj):
        return obj.get_absolute_url()

    def item_enclosure_mime_type(self):
        return "image/jpeg"

    def feed_copyright(self):
        return 'Copyright(c) ' + str(date.today().year) + ', StackTips'

    def item_pubdate(self, obj):
        return obj.published_date

    def item_categories(self, obj):
        return [category.slug for category in obj.category.all()]


class ArticlesRssFeed(BaseRssFeedView):
    title = "StackTips - Articles"
    link = "/articles"

    def item_enclosure_url(self, obj):
        thumbnail = "https://media.stacktips.com/media/uploads/stacktips-banner.png"
        if obj.thumbnail:
            thumbnail = settings.ASSETS_DOMAIN + obj.thumbnail.url
        return thumbnail

    def items(self):
        return Article.objects.filter(publish_status="LIVE").order_by('-published_date')[:30]

    def item_description(self, obj):
        content = f"{obj.content}\n<small>Originally published at <a href='{settings.SITE_URL + obj.get_absolute_url()}' target='_blank'>{settings.SITE_URL}</a></small>"

        thumbnail = "https://media.stacktips.com/media/uploads/stacktips-banner.png"
        if obj.thumbnail:
            thumbnail = settings.ASSETS_DOMAIN + obj.thumbnail.url
        return f'{content}<img src="{thumbnail}" alt="{obj.title}" style="display:none;">'

    def item_author_name(self, obj):
        author = obj.author
        return author.username if author else "StackTips"

    def item_author_link(self, obj):
        author = obj.author
        return settings.SITE_URL + obj.get_absolute_url() if author else "/"


class ArticleAtomFeed(ArticlesRssFeed):
    feed_type = ImageRssFeedGenerator
    subtitle = ArticlesRssFeed.description


class CoursesRssFeed(BaseRssFeedView):
    title = "StackTips - Courses"
    link = "/courses"

    def items(self):
        return Course.objects.filter(publish_status="LIVE").order_by('-published_date')[:30]

    def item_description(self, obj):
        content = f"{obj.excerpt}\n<small>Take the free course from <a href='{settings.SITE_URL + obj.get_absolute_url()}' target='_blank'>{settings.SITE_URL}</a></small>"
        return content

    def item_categories(self, obj):
        return []
