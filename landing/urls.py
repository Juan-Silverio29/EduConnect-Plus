#landing/urls.py

from django.urls import path
from . import views
from .views import home, user_info
from .views import login_api

urlpatterns = [
    path('', views.home, name='home'),
    path('api/user/', user_info, name='user_info'),
    path('api/login/', login_api, name='login_api'),
]

