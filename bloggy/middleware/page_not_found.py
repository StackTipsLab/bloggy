import logging

from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from bloggy import settings

logger = logging.getLogger(__name__)

fallback_404_url_mapping_new_site = {
    "/articles/how-to-configure-pojos-with-java-collection-attributes": "/articles/configure-pojos-with-java-collection-attributes-in-spring",
    "/courses/maven": "/courses/maven-for-beginners"
}


class PageNotFoundMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        request_path = request.path

        # Don't do anything for /api endpoints
        if request_path.startswith("/api/"):
            return response

        if response.status_code == 404:
            logger.warning("ERROR 404:: %s", request_path)
            if request_path in fallback_404_url_mapping_new_site:
                new_path = fallback_404_url_mapping_new_site[request_path]
                logger.warning("ERROR 404 Fallback:: %s ==> %s", request_path, new_path)
                return HttpResponsePermanentRedirect(settings.SITE_URL + new_path)

        return response
