import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

from django.conf import settings
from django.middleware.csrf import rotate_token
from django.utils.crypto import salted_hmac, constant_time_compare


cred = credentials.Certificate(settings.FIREBASE_PRIVATEKEY_FILE)
firebase_admin.initialize_app(cred)

FIREBASE_USER = 'firebase_user'
FIREBASE_SESSION_COOKIES = 'firebase_session_cookies'
USER_SESSION_HASH = 'user_hash'


class User:
    """
    Temporary user object have user attributes(mainly 'is_authenticated' for now).
    TODO: additional attributes and methods can be added.
    """
    is_authenticated = False
    is_anonymous = True
    
    def set_attributes(self, attr_dict):
        self.is_anonymous = False
        self.is_authenticated = True
        try:
            self.name = attr_dict['name']
        except KeyError:
            # There is not name for phone number auth
            self.name = ""
        
        
def generate_user_session_hash(session_cookies):
    key_salt = "django_firebase_authentication"
    return salted_hmac(key_salt, session_cookies)


def login(request, id_token):
    """
    Login the user and create session for the logged user.
    Keep user data in sessions
    """
    if not id_token:
        return
    
    try:
        decoded_token = auth.verify_id_token(id_token, check_revoked=True)
    except (auth.RevokedIdTokenError, auth.InvalidIdTokenError):
        return
    
    if FIREBASE_USER in request.session:
        if request.session[FIREBASE_USER]['uid'] != decoded_token['uid']:
            # avoid reusing another user session
            request.session.flush()
    else:
        request.session.cycle_key()
        
    session_cookies = auth.create_session_cookie(id_token, expires_in=datetime.timedelta(days=7))
    request.session[FIREBASE_SESSION_COOKIES] = session_cookies
    request.session[FIREBASE_USER] = decoded_token
    # request.session[USER_SESSION_HASH] = generate_user_session_hash(session_cookies)
    request.session.modified = True
    rotate_token(request)
    
    user = User()
    user.set_attributes(request.session[FIREBASE_USER])
    request.user = user
    
    
def logout(request):
    """
    Remove the user session data and make the user to unauthenticated user.
    """
    request.session.flush()
    request.user = User()
    
    
def get_user(request):
    """
    Return the firebase user instance associated with the given request session.
    If no user, return user with is_authenticated False
    """
    user = User()
    if FIREBASE_USER not in request.session:
        return user
    
    try:
        auth.verify_session_cookie(request.session[FIREBASE_SESSION_COOKIES], check_revoked=True)
        user.set_attributes(request.session[FIREBASE_USER])
    except auth.InvalidSessionCookieError:
        request.session.flush()
    
    return user
    
    
    
    
    