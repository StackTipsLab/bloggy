from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bloggy import models

DEFAULT_PAGE_SIZE = 20


def get_recent_feed(publish_status="LIVE", page=1, page_size=DEFAULT_PAGE_SIZE):
    articles = models.Post.objects.prefetch_related("category") \
        .filter(publish_status=publish_status) \
        .filter(post_type__in=["article", 'lesson']) \
        .order_by("-published_date")

    paginator = Paginator(articles, page_size)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return articles


def get_recent_posts(publish_status="LIVE", page=1, page_size=DEFAULT_PAGE_SIZE):
    articles = models.Post.objects.prefetch_related("category") \
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
