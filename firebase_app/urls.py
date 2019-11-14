from django.urls import path

from .views import *


app_name = 'firebase_app'

urlpatterns = [
    path('login_view/', LoginView.as_view(), name='login_view'),
    path('', HomeView.as_view(), name='index'),
    path('logout/', LogoutView.as_view(), name='logout')
    ]