import json

from django.http import HttpRequest

from bloggy import settings


def seo_attrs(request: HttpRequest):
    """returns seo attributes to be merged into the context
    Arguments:
        request {HttpRequest} -- request object
    """
    with open('seo_settings.json', 'r', encoding='utf-8') as seo_file:
        seo_settings = json.load(seo_file)

        # Default SEO attributes
        seo = {
            'seo_site_name': settings.SITE_TITLE,
            'seo_title': settings.SITE_TAGLINE,
            'seo_description': settings.SITE_DESCRIPTION,
            'og_image': settings.SITE_LOGO,
            'seo_image': settings.SITE_LOGO
        }

        # Get SEO attributes based on the request path
        request_path = request.path
        if request_path in seo_settings:
            seo.update(seo_settings[request_path])

    return seo


def app_settings(request: HttpRequest):
    """
        returns app settings
    """
    return {
        "DEVELOPMENT_MODE": settings.DEVELOPMENT_MODE,
        "ASSETS_DOMAIN": settings.ASSETS_DOMAIN
    }
