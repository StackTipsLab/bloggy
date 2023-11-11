from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bloggy.models import Post, Quiz

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
    context["meta_title"] = meta_title

    meta_description = self.object.meta_description
    if StringUtils.is_blank(meta_description) or meta_description == "{excerpt}":
        meta_description = self.object.excerpt
    context["meta_description"] = meta_description
    context['meta_keywords'] = self.object.meta_keywords
    if self.object.thumbnail:
        context['meta_image'] = self.object.thumbnail.url