
import json
import datetime
from pathlib import Path 

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TokenForm

# Create your views here.

cred = credentials.Certificate('./firebase_app/AdmingSDK.json')
default_app = firebase_admin.initialize_app(cred)


class LoginView(generic.FormView):
    form_class = TokenForm
    template_name = "register/login.html"
    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            id_token = form.cleaned_data['token']
            try:
                decoded_token = auth.verify_id_token(id_token, check_revoked=True)
                request.session['firebase_user'] = decoded_token
            except (auth.RevokedIdTokenError, auth.InvalidIdTokenError):
                pass # redirect to login page with error message
            else:
                session_cookies = auth.create_session_cookie(id_token, expires_in=datetime.timedelta(days=14))
                request.session['firebase_session_cookies'] = session_cookies
                request.session.modified = True
            return HttpResponseRedirect("/")
        else:
            print(form.errors)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        with Path('./firebase_app/firebase_app_config.json').open() as fp:
            context['firebaseConfig'] = json.load(fp)
        return context
            

class HomeView(generic.View):
    def get(self, request):
        session_cookie = request.session.get('firebase_session_cookies')
        if session_cookie:
            try:
                auth.verify_session_cookie(session_cookie, check_revoked=True)
                return HttpResponse("Logged in")
            except auth.InvalidSessionCookieError:
                pass
        return HttpResponseRedirect('/login_view')

    
class LogoutView(generic.View):
    def get(self, request):
        request.session.flush()
        return HttpResponseRedirect('/login_view')
        
            
