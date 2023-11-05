# myproject.middleware.py
import logging

from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from bloggy import settings

logger = logging.getLogger(__name__)


# fallback_404_url_mapping_old_site = {
#     "/tutorials/spring/how-to-configure-pojos-with-java-collection-attributes": "/articles/configure-pojos-with-java-collection-attributes-in-spring",
#     "/android/download-and-display-image-in-android-gridview": "/articles/download-and-display-image-in-android-gridview",
#     "/article/how-to-format-your-post": "/how-to-format-your-post",
#     "/android/android-framelayout-example": "/articles/android-framelayout-example",
#     "/interview-questions": "/articles",
#     "/courses/maven": "/courses/maven-for-beginners",
#     "/how-to-format-your-post": "/contribute",
#     "/article/download-and-display-image-in-android-gridview": "/articles/download-and-display-image-in-android-gridview"
# }

# paths_to_replace = [
#     "/tutorials/java/spring/",
#     "/tutorials/android/",
#     "/tutorials/spring-boot/",
#     "/tutorials/spring/",
#     "/tutorials/laravel/",
#     "/tutorials/php/",
#     "/tutorials/git/",
#     "/tutorials/html5/",
#     "/tutorials/bootstrap/",
#     "/tutorials/java/",
#     "/tutorials/xamarin/",
#     "/tutorials/react/",
#     "/tutorials/react-native/",
#     "/tutorials/wordpress/",
#     "/tutorials/json/",
#     "/tutorials/design-patterns/",
#     "/tutorials/sencha-touch/",
#     "/tutorials/ibm-worklight/",
#     "/tutorials/phonegap/",
#     "/tutorials/ios/",
#     "/tutorials/seo/",
#     "/tutorials/se-concepts/",
#     "/tutorials/servlets/",
#     "/tutorials/struts/",
#     "/tutorials/c/",
#     "/tutorials/struts/",
#     "/tutorials/libgdx/",
#     "/how-to/",
#     "/blog/",
# ]

class UrlRedirectMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        request_path = request.path

        # Don't do anything for /api endpoints
        # if request_path.startswith("/api/"):
        #     return response
        # if request_path.startswith("/tutorials/blackberry/") or request_path.startswith("/tutorials/j2me/"):
        #     new_path = reverse("articles")
        #     logger.warning("WPRedirect:: %s->%s", request_path, new_path)
        #     return HttpResponsePermanentRedirect(settings.SITE_URL + new_path)
        #
        # if request_path in fallback_404_url_mapping_old_site:
        #     new_path = fallback_404_url_mapping_old_site[request_path]
        #     logger.warning("WPRedirect:: %s->%s", request_path, new_path)
        #     return HttpResponsePermanentRedirect(settings.SITE_URL + new_path)
        #
        # if request_path.startswith("/courses/maven/"):
        #     new_path = request_path.replace(request_path, "/courses/maven-for-beginners/")
        #     logger.warning("WPRedirect:: %s->%s", request_path, new_path)
        #     return HttpResponsePermanentRedirect(settings.SITE_URL + new_path)
        #
        # for ptr in paths_to_replace:
        #     if request_path.startswith(ptr):
        #         new_path = request_path.replace(ptr, "/articles/")
        #         logger.warning("WPRedirect:: %s->%s", request_path, new_path)
        #         return HttpResponsePermanentRedirect(settings.SITE_URL + new_path)

        return response
