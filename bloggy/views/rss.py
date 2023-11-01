from datetime import date

from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from django.template.context_processors import static
from bloggy import settings
from bloggy.models import Post
from bloggy.models.course import Course


class ImageRssFeedGenerator(feedgenerator.Rss201rev2Feed):
    def add_root_elements(self, handler):
        super().add_root_elements(handler)

        handler.startElement('image', {})
        handler.addQuickElement("url", self.feed['logo'])
        handler.addQuickElement("title", self.feed['title'])
        handler.addQuickElement("link", self.feed['link'])
        handler.endElement('image')


class BaseRssFeedView(Feed):
    feed_type = ImageRssFeedGenerator
    content_type = 'application/xml; charset=utf-8'
    description = f'most recent posts from {settings.SITE_TITLE}'
    language = "en"

    def feed_extra_kwargs(self, obj):
        return {
            'logo': settings.SITE_LOGO,
            'icon': static('static/media/logo.png')
        }

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_enclosure_mime_type(self):
        return "image/jpeg"

    def feed_copyright(self):
        return f'Copyright(c) {str(date.today().year)} {settings.SITE_TITLE}'

    def item_pubdate(self, item):
        return item.published_date

    def item_categories(self, obj):
        return [category.slug for category in obj.category.all()]


class PostsRssFeed(BaseRssFeedView):
    title = f'Posts from {settings.SITE_TITLE}'
    link = "/articles"

    def item_enclosure_url(self, item):
        thumbnail = static('static/media/default-banner.png')
        if item.thumbnail:
            thumbnail = settings.ASSETS_DOMAIN + item.thumbnail.url
        return thumbnail

    def items(self):
        return Post.objects.filter(publish_status="LIVE").order_by('-published_date')[:30]

    def item_description(self, item):
        content = (f"{item.content}\n<small>Originally published at "
                   f"<a href='{settings.SITE_URL + item.get_absolute_url()}' "
                   f"target='_blank'>{settings.SITE_URL}</a></small>")

        thumbnail = static('static/media/default-banner.png')
        if item.thumbnail:
            thumbnail = settings.ASSETS_DOMAIN + item.thumbnail.url
        return f'{content}<img src="{thumbnail}" alt="{item.title}" style="display:none;">'

    def item_author_name(self, item):
        author = item.author
        return author.username if author else None

    def item_author_link(self, item):
        author = item.author
        return settings.SITE_URL + item.get_absolute_url() if author else "/"


class ArticleAtomFeed(PostsRssFeed):
    feed_type = ImageRssFeedGenerator
    subtitle = PostsRssFeed.description


class CoursesRssFeed(BaseRssFeedView):
    title = "Courses"
    link = "/courses"

    def items(self):
        return Course.objects.filter(publish_status="LIVE").order_by('-published_date')[:30]

    def item_description(self, item):
        content = f"{item.excerpt}\n<small>Take the free course from <a href='{settings.SITE_URL + item.get_absolute_url()}' target='_blank'>{settings.SITE_URL}</a></small>"
        return content

    def item_categories(self, obj):
        return []
