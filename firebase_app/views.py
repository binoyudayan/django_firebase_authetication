
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
from .auth import login, logout

# Create your views here.

class LoginView(generic.FormView):
    form_class = TokenForm
    template_name = "register/login.html"
    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            id_token = form.cleaned_data['token']
            login(request, id_token)
            return HttpResponseRedirect("/")
        else:
            return self.form_invalid(form)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        with Path('./firebase_app/firebase_app_config.json').open() as fp:
            context['firebaseConfig'] = json.load(fp)
        return context
            

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "firebase_app/index.html"

    
class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login_view')
        
            
