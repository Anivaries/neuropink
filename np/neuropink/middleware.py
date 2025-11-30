import logging

logger = logging.getLogger('django.request')


class Log400Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 400:
            logger.warning(
                f'400 Bad Request: {request.method} {request.path} '
                f'Host: {request.get_host()} '
                f'User-Agent: {request.META.get("HTTP_USER_AGENT", "")}'
            )

        return response
