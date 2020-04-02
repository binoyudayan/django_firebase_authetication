import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

from django.conf import settings
from django.middleware.csrf import rotate_token
from django.utils.crypto import salted_hmac

from common_utils.utils import wait_for_doc
from firebase_authentication import *
from firebase_authentication.functions import update_profile
from .firestore_documents import User


class AuthenticationError(Exception): 
    pass

       
        
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
    
                    
    if not decoded_token.get('email_verified'):
        logger.debug("login: email not verified.")
        raise AuthenticationError("email not verified") 
    
    if FIREBASE_USER in request.session:
        if request.session[FIREBASE_USER]['uid'] != decoded_token['uid']:
            # avoid reusing another user session
            request.session.flush()
    else:
        request.session.cycle_key()

    logger.debug("login: check session completed")
    # session validity is set to id token validity, so that cloud function
    # calls wont due to authentication (401 error)
    session_cookies = auth.create_session_cookie(id_token, expires_in=datetime.timedelta(hours=1))
    logger.debug("login: cookie created")
    
    request.session[FIREBASE_SESSION_COOKIES] = session_cookies
    request.session[USER_TOKEN] = id_token
    update_user_attr(request, decoded_token)
    
    profile_doc = firestore_db.collection(u'users').document(decoded_token['uid'])
    logger.debug("login: Get profile doc") # no uids in log 
    profile = wait_for_doc(profile_doc).to_dict()
    logger.debug("login: Got profile data")
        
    request.session[FIREBASE_USER].update(profile)
    request.session.modified = True
    rotate_token(request)
    
    user = User()
    user.set_attributes(request.session[FIREBASE_USER])
    request.user = user
    
    
def logout(request):
    """
    Remove the user session data and make the user to unauthenticated user.
    """
    if save:
        # save changes in profile before logout if valid session
        request.user.save(request)
    
    try:
        decoded_claims = auth.verify_session_cookie(request.session[FIREBASE_SESSION_COOKIES])
        auth.revoke_refresh_tokens(decoded_claims['sub'])
    except auth.InvalidSessionCookieError:
        pass
    
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
    
    
    
    
    
