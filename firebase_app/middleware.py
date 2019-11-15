
from django.utils.deprecation import MiddlewareMixin

from .auth import get_user


class FirebaseAuthenticationMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Firebase authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'firebase_app.middleware.FirebaseAuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = get_user(request)