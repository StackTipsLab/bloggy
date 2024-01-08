from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bloggy.models import Post, Quiz
from bloggy.utils.string_utils import StringUtils
from bs4 import BeautifulSoup

DEFAULT_PAGE_SIZE = 20


def get_recent_feed(publish_status="LIVE", page=1, page_size=DEFAULT_PAGE_SIZE):
    posts = Post.objects.prefetch_related("category") \
        .filter(publish_status=publish_status) \
        .order_by("-published_date")

    paginator = Paginator(posts, page_size)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


def get_recent_posts(publish_status="LIVE", page=1, page_size=DEFAULT_PAGE_SIZE):
    articles = Post.objects.prefetch_related("category") \
        .filter(publish_status=publish_status).filter(post_type__in=["article"]) \
        .order_by("-published_date")

    paginator = Paginator(articles, page_size)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return articles


def get_recent_quizzes(publish_status="LIVE", page=1):
    quizzes = Quiz.objects.prefetch_related("category") \
        .filter(publish_status=publish_status).order_by("-published_date")
    paginator = Paginator(quizzes, DEFAULT_PAGE_SIZE)
    try:
        quizzes = paginator.page(page)
    except PageNotAnInteger:
        quizzes = paginator.page(1)
    except EmptyPage:
        quizzes = paginator.page(paginator.num_pages)

    return quizzes


def set_seo_settings(post, context):
    if StringUtils.is_blank(post.meta_title):
        context["meta_title"] = post.title
    else:
        context["meta_title"] = post.meta_title

    if StringUtils.is_blank(post.meta_description):
        context["meta_description"] = post.excerpt
    else:
        context["meta_description"] = post.meta_description
    context['meta_keywords'] = post.meta_keywords

    if post.thumbnail:
        context['meta_image'] = post.thumbnail.url


def cleanse_html(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    for tag in soup.find_all(True, {'style': True}):
        del tag['style']

    # Find and remove empty <p>, <a>, and <span> tags
    for tag in soup.find_all(['p', 'a', 'span']):
        if not tag and (not tag.contents or (len(tag.contents) == 1 and not tag.contents[0].strip())):
            tag.extract()

    # Get the modified HTML string
    return str(soup)
