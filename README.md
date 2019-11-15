# django_firebase_authetication
Google firebase : https://firebase.google.com/ <br>
A simple django application to use google firebase <a href="https://firebase.google.com/">authetication</a> and <a href="https://firebase.google.com/docs/auth/admin">admin SDK</a> to authenticate users and managing user <a href="https://docs.djangoproject.com/en/2.2/topics/http/sessions/">sessions</a>.

The main objective of this project is to not have User model. And directly use firebase authentication feature. But still using django sessions for user session handling.

<h3>Using the app</h3>
  1. Create a django project and the repository inside that <br>
  2. Install all the dependencies using requirements.txt <br>
  3. Add the application in INSTALLED_APPS. <code>django.contrib.admin</code> and <code>django.contrib.auth.middleware.AuthenticationMiddleware</code> can be commented.<br>
  4. Add <code>FIREBASE_PRIVATEKEY_FILE</code> to settings with path of Admin sdk private key json file
  5. Add <code>firebase_app.middleware.FirebaseAuthenticationMiddleware</code> to <code>MIDDLEWARE</code> after sessions middleware<br>
  <code>
  MIDDLEWARE = [
    ...,
    'firebase_app.middleware.FirebaseAuthenticationMiddleware',
    ...
  ]
  </code>
  6. Copy firebase app config json files to the app if you would like use the example in views.py<br>

We can make it as a reusable project with middleware for firebase authentication with django without Django user models, permissions etc. At the moment, the app has only three views login and logout and a home. Login and logout can be reusabe and the logic in home view can be moved to middleware process response.

<b> The code is not verified by any experts. You can contribute or suggest for improvements.</b>
