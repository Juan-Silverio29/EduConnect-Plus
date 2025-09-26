#dashboard/urls.py
#dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('profesor/', views.dashboard_profesor, name='dashboard_profesor'),
]
