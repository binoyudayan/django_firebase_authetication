
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings 

from .auth import get_user


class FirebaseAuthenticationMiddleware1(MiddlewareMixin):
    
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Firebase authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'firebase_app.middleware.FirebaseAuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = get_user(request)
        
        
class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.user = get_user(request)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
