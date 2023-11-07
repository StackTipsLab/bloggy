from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bloggy import models
from bloggy.models import Quiz

DEFAULT_PAGE_SIZE = 20


def get_recent_feed(publish_status="LIVE", page=1, page_size=DEFAULT_PAGE_SIZE):
    posts = models.Post.objects.prefetch_related("category") \
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
