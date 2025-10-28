# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboards principales
    path('', views.dashboard_view, name='dashboard'),
    path('user/', views.dashboard_user, name='dashboard_user'),
    path('profesor/', views.dashboard_profesor, name='dashboard_profesor'),
    path('admin-panel/', views.dashboard_admin, name='dashboard_admin'),

    # Profesor
    path('profesor/cursos/', views.profesor_cursos, name='profesor_cursos'),
    path('profesor/evaluaciones/', views.profesor_evaluaciones, name='profesor_evaluaciones'),
    path('profesor/material/', views.profesor_material, name='profesor_material'),
    path('profesor/material/editar/<int:id>/', views.editar_material_view, name='editar_material'),
    path('profesor/material/eliminar/<int:id>/', views.eliminar_material_view, name='eliminar_material'),
    path('profesor/foros/', views.foros_profesor, name='foros_profesor'),

    # Admin
    path('admin/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin/cursos/', views.admin_cursos, name='admin_cursos'),
    path('admin/estadisticas/', views.admin_estadisticas, name='admin_estadisticas'),

    # Prueba JWT (opcional)
    #path('prueba/', views.prueba_jwt, name='prueba-jwt'),
]
