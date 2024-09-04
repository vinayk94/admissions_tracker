from django.db import connection

class ThreadLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        connection.close()
        response = self.get_response(request)
        return response