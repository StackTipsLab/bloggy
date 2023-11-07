import logging

from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin

from bloggy import settings
from bloggy.models import RedirectRule

logger = logging.getLogger(__name__)


class RedirectMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        request_path = request.path

        # Don't do anything for /api endpoints
        if request_path.startswith("/api/"):
            return response

        if response.status_code == 404:
            logger.warning("ERROR 404:: %s", request_path)
            redirect_rule = RedirectRule.objects.filter(source__exact=request_path).first()

            if redirect_rule:
                logger.warning("Explicit redirect rule found %s ==> %s", redirect_rule.source,
                               redirect_rule.destination)
                return HttpResponsePermanentRedirect(settings.SITE_URL + redirect_rule.destination)

        return response
