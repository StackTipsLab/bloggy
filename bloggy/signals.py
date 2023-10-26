import urllib.parse
from urllib import request

import django.core
from django.db.models.signals import post_save
from django.dispatch import receiver

import bloggy.models
from bloggy import settings

PING_GOOGLE_URL = "https://www.google.com/webmasters/tools/ping"
INDEX_NOW = "https://www.bing.com/indexnow?url={}&key={}"


@receiver(post_save, sender=bloggy.models.Article)
def post_saved_action_signal(sender, instance, created, **kwargs):
    # Update category count everytime three is a new object added
    if created:
        print(f"Sendr:{sender}, kwargs:{kwargs}")
        django.core.management.call_command('update_category_count')

    if instance.publish_status == "PUBLISHED":
        if settings.PING_GOOGLE_POST_UPDATE:
            ping_google()

        if settings.PING_INDEX_NOW_POST_UPDATE:
            ping_index_now(instance)


def ping_google():
    try:
        params = urllib.parse.urlencode({"sitemap": settings.SITE_URL + "/sitemap.xml"})
        response = request.urlopen(f"{PING_GOOGLE_URL}?{params}")
        if response.code == 200:
            print("Successfully pinged this page for Google!")
    except Exception:
        print("Error while pinging google")


def ping_index_now(article):
    try:
        response = request.urlopen(
            INDEX_NOW.format(article.get_absolute_url(), settings.INDEX_NOW_API_KEY))
        if response.code == 200:
            print("Successfully pinged this page for IndexNow!")
    except Exception:
        print("Error while pinging google")
