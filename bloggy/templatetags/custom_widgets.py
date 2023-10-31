import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from numerize.numerize import numerize

from bloggy.models import Vote, Bookmark, Post, Category, Option

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    if value > 0:
        dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def get_youtube_channel_id(url):
    pattern = r'channel/([A-Za-z0-9_\-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


@register.simple_tag
def sanitize_url(url):
    if url is None:
        return url

    if not re.match('(?:http|https)://', url):
        return f'https://{url}'
    return url


@register.simple_tag
def convert_to_absolute_url(url, root):
    if url is None:
        return url

    domain = get_domain(root)
    if domain not in url:
        return "https://" + domain + url

    return url


@register.simple_tag
def format_number(num):
    return numerize(num)


@register.simple_tag
def check_if_user_bookmarked(post_id, post_type, user):
    if user.is_authenticated:
        return Bookmark.objects.filter(post_id=post_id, post_type=post_type, user=user).count()
    return 0


@register.simple_tag
def check_if_user_voted(post_id, post_type, user):
    if user.is_authenticated:
        return Vote.objects.filter(post_id=post_id, post_type=post_type, user=user).count()
    return 0


@register.simple_tag
def get_domain(website):
    domain = urlparse(website).netloc
    return domain.replace("www.", "")


@register.simple_tag
def get_twitter_username(twitter_url):
    regex = r"^https?:\/\/(?:www\.)?twitter\.com\/(?:#!\/)?@?([^/?#]*)(?:[?#].*)?$"
    result = re.findall(regex, twitter_url)
    if result:
        return result[0]
    return twitter_url


@register.simple_tag
def get_github_username(github_url):
    regex = r"^https?:\/\/(?:www\.)?github\.com\/(?:#!\/)?@?([^/?#]*)(?:[?#].*)?$"
    result = re.findall(regex, github_url)
    if result:
        return result[0]
    return github_url


@register.simple_tag
def format_date(dt=False, date_format='%Y-%m-%d %H:%M:%S'):
    if dt is None:
        return ""
    return datetime.today().strftime(date_format)


@register.simple_tag
def pretty_date(dt=None):
    """
       Get a datetime object or a int() Epoch timestamp and return a
       pretty string like 'an hour ago', 'Yesterday', '3 months ago',
       'just now', etc
       """
    if dt is None:
        return ""

    now = datetime.now(timezone.utc)

    if isinstance(dt, int):
        dt = datetime.fromtimestamp(dt)

    diff = now - dt
    seconds_diff = diff.total_seconds()
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if seconds_diff < 10:
        return "just now"
    if seconds_diff < 60:
        return f"{int(seconds_diff)} seconds ago"
    if seconds_diff < 3600:
        minutes_diff = int(seconds_diff / 60)
        return f"{minutes_diff} minute{'s' if minutes_diff > 1 else ''} ago"
    if seconds_diff < 86400:
        hours_diff = int(seconds_diff / 3600)
        return f"{hours_diff} hour{'s' if hours_diff > 1 else ''} ago"
    if day_diff == 1:
        return "yesterday"
    if day_diff < 7:
        return f"{day_diff} day{'s' if day_diff > 1 else ''} ago"
    if day_diff < 31:
        weeks_diff = int(day_diff / 7)
        return f"{weeks_diff} week{'s' if weeks_diff > 1 else ''} ago"
    if day_diff < 365:
        months_diff = int(day_diff / 30)
        return f"{months_diff} month{'s' if months_diff > 1 else ''} ago"
    years_diff = int(day_diff / 365)
    return f"{years_diff} year{'s' if years_diff > 1 else ''} ago"




@register.inclusion_tag('widgets/related_article_widget.html', takes_context=True)
def related_article_widget(context, count=12, categories=None, slug=0, widget_title="Related posts",
                           widget_style="list"):
    articles = None
    if categories is None:
        articles = Post.objects.filter(publish_status="LIVE").filter(post_type="article") \
                       .exclude(slug=slug).order_by('-published_date')[:count].all()
        categories = []

    category_slugs = []
    for category in categories:
        category_slugs.append(str(category.slug))

    if len(category_slugs) > 0:
        articles = Post.objects.filter(category__slug__in=category_slugs, publish_status="LIVE").filter(
            post_type="article") \
                       .exclude(slug=slug).order_by('-published_date')[:count].all()

    return {
        "widgetTitle": widget_title,
        "relatedArticles": articles,
        "widgetStyle": widget_style,
    }


@register.inclusion_tag('widgets/categories_widget.html', takes_context=True)
def categories_widget(context, content_type="article", count=0, widget_style=""):
    categories = Category.objects.filter(article_count__gt=0).order_by("-article_count").all()

    return {
        "categories": categories,
        "widgetStyle": widget_style,
        "contentType": content_type
    }


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def replace_all(pattern, repl, string) -> str:
    occurences = re.findall(pattern, string, re.IGNORECASE)
    for occurence in occurences:
        string = string.replace(occurence, repl)
        return string


@register.filter
def highlight_search(text, search):
    highlighted = text.replace(
        search, f'<span class="highlight">{search}</span>')
    return mark_safe(highlighted)


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.simple_tag
def get_options(keys=None):
    if keys is None:
        keys = []
    return Option.objects.filter(key__in=keys).get()


@register.simple_tag
def get_option(key):
    try:
        return Option.objects.filter(key=key).get()
    except Option.DoesNotExist:
        return None


@register.simple_tag
def get_option_safe(key):
    if key is None:
        return "Invalid key"

    option_from_db = get_option(key)
    return mark_safe(
        "<input type=\"hidden\" value=\"Option Does Not Exist!\">" if option_from_db is None else option_from_db.value)


@register.simple_tag
def get_settings(name):
    return getattr(settings, name, "")


@register.simple_tag
def slugify(username):
    username = slugify(username.replace(".", "_").lower())
    return username.replace("-", "_")
