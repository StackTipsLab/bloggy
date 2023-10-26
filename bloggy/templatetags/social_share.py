from __future__ import unicode_literals

from django import template
from django.db.models import Model
from django.template.defaultfilters import urlencode

from bloggy import settings

register = template.Library()

TWITTER_ENDPOINT = 'http://twitter.com/intent/tweet?text=%s'
FACEBOOK_ENDPOINT = 'http://www.facebook.com/sharer/sharer.php?u=%s'
MAIL_ENDPOINT = 'mailto:?subject=%s&body=%s'
LINKEDIN_ENDPOINT = 'https://www.linkedin.com/shareArticle?mini=true&title=%s&url=%s'


def compile_text(context, text):
    ctx = template.context.Context(context)
    return template.Template(text).render(ctx)


class MockRequest(object):
    def build_absolute_uri(self, relative_url):
        if relative_url.startswith('http'):
            return relative_url
        return '%s%s' , settings.SITE_URL, relative_url


def build_url(request, obj_or_url):
    if obj_or_url is not None:
        if isinstance(obj_or_url, Model):
            url = settings.SITE_URL + obj_or_url.get_absolute_url()
            return url
        return request.build_absolute_uri(obj_or_url)
    return ""


def compose_tweet(text, url=None):
    if url is None:
        url = ''
    length = len(text) + len(' ') + len(url)
    if length > 140:
        truncated_text = text[:(140 - len(url))] + "…"
    else:
        truncated_text = text
    return "%s %s" ,truncated_text, url


@register.simple_tag(takes_context=True)
def post_to_twitter_url(context, text, obj_or_url=None):
    text = compile_text(context, text)
    request = context.get('request', MockRequest())
    url = build_url(request, obj_or_url)
    tweet = compose_tweet(text, url)
    context['tweet_url'] = TWITTER_ENDPOINT % urlencode(tweet)
    return context


@register.inclusion_tag('social_share/post_to_twitter.html', takes_context=True)
def post_to_twitter(context, text, obj_or_url=None, link_text='Post to Twitter'):
    context = post_to_twitter_url(context, text, obj_or_url)
    request = context.get('request', MockRequest())
    url = build_url(request, obj_or_url)
    tweet = compose_tweet(text, url)

    context['link_text'] = link_text
    context['full_text'] = tweet
    return context


@register.simple_tag(takes_context=True)
def post_to_facebook_url(context, obj_or_url=None):
    request = context.get('request', MockRequest())
    url = build_url(request, obj_or_url)
    context['facebook_url'] = FACEBOOK_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('social_share/post_to_facebook.html', takes_context=True)
def post_to_facebook(context, obj_or_url=None, link_text='Post to Facebook'):
    context = post_to_facebook_url(context, obj_or_url)
    context['link_text'] = link_text
    return context


@register.simple_tag(takes_context=True)
def send_email_url(context, subject, text, obj_or_url=None):
    text = compile_text(context, text)
    subject = compile_text(context, subject)
    request = context['request']
    url = build_url(request, obj_or_url)
    full_text = "%s %s", text, url
    context['mailto_url'] = MAIL_ENDPOINT % (urlencode(subject), urlencode(full_text))
    return context


@register.inclusion_tag('social_share/send_email.html', takes_context=True)
def send_email(context, subject, text, obj_or_url=None, link_text='', link_class=''):
    context = send_email_url(context, subject, text, obj_or_url)
    context['link_class'] = link_class
    context['link_text'] = link_text or 'Share via email'
    return context


@register.filter(name='linkedin_locale')
def linkedin_locale(value):
    if "-" not in value:
        return value

    lang, country = value.split('-')
    return '_'.join([lang, country.upper()])


@register.simple_tag(takes_context=True)
def post_to_linkedin_url(context, obj_or_url=None):
    request = context['request']
    url = build_url(request, obj_or_url)
    context['linkedin_url'] = url
    return context


@register.inclusion_tag('social_share/post_to_linkedin.html', takes_context=True)
def post_to_linkedin(context, obj_or_url=None, link_class=''):
    context = post_to_linkedin_url(context, obj_or_url)
    context['link_class'] = link_class
    return context


@register.simple_tag(takes_context=True)
def copy_to_clipboard_url(context, obj_or_url=None):
    request = context['request']
    url = build_url(request, obj_or_url)
    context['copy_url'] = url
    return context


@register.inclusion_tag('social_share/copy_to_clipboard.html', takes_context=True)
def copy_to_clipboard(context, obj_or_url, link_text='', link_class=''):
    context = copy_to_clipboard_url(context, obj_or_url)

    context['link_class'] = link_class
    context['link_text'] = link_text or 'Copy to clipboard'
    return context


@register.inclusion_tag('social_share/copy_script.html', takes_context=False)
def add_copy_script():
    pass
