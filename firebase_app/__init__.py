
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore
from firebase_admin import storage

from django.conf import settings

if not (len(firebase_admin._apps)):
    # avoid initializing more than once
    cred = credentials.Certificate(settings.FIREBASE_PRIVATEKEY_FILE)
    firebase_admin.initialize_app(cred)
    
firestore_db = firestore.client()
storage_bucket = storage.bucket(name=settings.FIREBASE_BUCKET_NAME)


FIREBASE_USER = 'firebase_user'
FIREBASE_SESSION_COOKIES = 'firebase_session_cookies'
USER_SESSION_HASH = 'user_hash'
USER_ACTIVE_KEY = 'active'
USER_TOKEN = 'id_token'


__all__ = ['firestore_db', 'storage_bucket', 'FIREBASE_USER',
           'FIREBASE_SESSION_COOKIES', 'USER_ACTIVE_KEY', 'USER_TOKEN']
