from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

class ErrorMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):

        logger.error(
            f'Error no capturado: {str(exception)}',
            exc_info=True
        )

        return render(
            request,
            'solicitudes/error.html',
            {
                'status_code': 500,
                'error_title': 'Error del servidor'
            },
            status=500
        )