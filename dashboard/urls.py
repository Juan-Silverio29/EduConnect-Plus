#dashboard/urls.py
#dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path("user/", views.dashboard_user, name="dashboard_user"),
    path('profesor/', views.dashboard_profesor, name='dashboard_profesor'),

    path('prueba/', views.prueba_jwt, name='prueba-jwt'),
    path('profesor/cursos/', views.profesor_cursos, name='profesor_cursos'),
    path('profesor/cursos/', views.profesor_cursos, name='profesor_cursos'),
    path('profesor/evaluaciones/', views.profesor_evaluaciones, name='profesor_evaluaciones'),
    path('profesor/material/', views.profesor_material, name='profesor_material'),
    



]

