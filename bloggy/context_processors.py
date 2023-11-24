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
            'site_name': settings.SITE_TITLE,
            'meta_title': settings.SITE_TAGLINE,
            'meta_description': settings.SITE_DESCRIPTION,
            'meta_image': settings.SITE_LOGO
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
        "LOAD_GOOGLE_TAG_MANAGER": settings.LOAD_GOOGLE_TAG_MANAGER,
        "LOAD_GOOGLE_ADS": settings.LOAD_GOOGLE_ADS,
        "ASSETS_DOMAIN": settings.ASSETS_DOMAIN
    }
