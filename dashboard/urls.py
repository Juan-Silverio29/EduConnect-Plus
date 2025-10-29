# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

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
    path('profesor/crear_curso/', views.crear_curso, name='crear_curso'),
    path('profesor/curso/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('profesor/curso/editar/<int:curso_id>/', views.editar_curso, name='editar_curso'),
    path('profesor/material/asignar/<int:material_id>/', views.asignar_material_a_curso, name='asignar_material_a_curso'),
    path('profesor/evaluaciones/crear/', views.crear_evaluacion, name='crear_evaluacion'),
    path('profesor/evaluaciones/editar/<int:evaluacion_id>/', views.editar_evaluacion, name='editar_evaluacion'),
    path('profesor/evaluaciones/eliminar/<int:evaluacion_id>/', views.eliminar_evaluacion, name='eliminar_evaluacion'),
    path('profesor/evaluaciones/detalle/<int:evaluacion_id>/', views.detalle_evaluacion, name='detalle_evaluacion'),
    path('profesor/evaluaciones/<int:evaluacion_id>/quitar/<int:material_id>/', views.quitar_material_evaluacion, name='quitar_material_evaluacion'),

    # Alumno
    path('user/cursos/', views.cursos_disponibles, name='cursos_disponibles'),
    path('user/inscribirse/<int:curso_id>/', views.inscribirse_curso, name='inscribirse_curso'),
    path('user/mis_recursos/', views.mis_recursos, name='mis_recursos'),

    # IA (solo profesor y alumno)
    path('ai/stats/', views.ai_stats_api, name='ai_stats'),
    path('ai/recs/', views.ai_recommendations_api, name='ai_recommendations'),
    path('ai/chat/', views.ai_chat_api, name='ai_chat'),

    # Admin
    path('admin/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin/cursos/', views.admin_cursos, name='admin_cursos'),
    path('admin/estadisticas/', views.admin_estadisticas, name='admin_estadisticas'),
    path('admin/distribucion-usuarios/', views.admin_user_distribution, name='admin_user_distribution'),
    path('admin/distribucion-usuarios/', views.admin_user_distribution, name='admin_distribution'),
    # path('admin/distribution/', views.admin_distribution_view, name='admin_distribution'),  # Esta línea está comentada porque tienes dos funciones similares
]