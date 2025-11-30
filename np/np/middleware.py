import logging
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseBadRequest

logger = logging.getLogger('django.request')


class LogBadRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except SuspiciousOperation as e:
            logger.error(f"400 Bad Request: {e}", exc_info=True)
            return HttpResponseBadRequest("Bad Request")
        return response
