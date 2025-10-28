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
    path('profesor/evaluaciones/', views.profesor_evaluaciones, name='profesor_evaluaciones'),
    path('profesor/material/', views.profesor_material, name='profesor_material'),
    path('profesor/material/editar/<int:id>/', views.editar_material_view, name='editar_material'),
    path('profesor/material/eliminar/<int:id>/',views.eliminar_material_view, name='eliminar_material'),
    path('profesor/foros/', views.foros_profesor, name='foros_profesor'),
    path("profesor/crear_curso/", views.crear_curso, name="crear_curso"),
    path("user/cursos/", views.cursos_disponibles, name="cursos_disponibles"),
    path("user/inscribirse/<int:curso_id>/", views.inscribirse_curso, name="inscribirse_curso"),
    path("user/mis_recursos/", views.mis_recursos, name="mis_recursos"),
    path("profesor/crear_curso/", views.crear_curso, name="crear_curso"),
    path("profesor/curso/<int:curso_id>/", views.detalle_curso, name="detalle_curso"),
    path("profesor/curso/editar/<int:curso_id>/", views.editar_curso, name="editar_curso"),
    path('profesor/material/asignar/<int:material_id>/', views.asignar_material_a_curso, name='asignar_material_a_curso'),
    path('profesor/evaluaciones/', views.profesor_evaluaciones, name='profesor_evaluaciones'),
    path('profesor/evaluaciones/crear/', views.crear_evaluacion, name='crear_evaluacion'),
    path('profesor/evaluaciones/editar/<int:evaluacion_id>/', views.editar_evaluacion, name='editar_evaluacion'),
    path('profesor/evaluaciones/eliminar/<int:evaluacion_id>/', views.eliminar_evaluacion, name='eliminar_evaluacion'),
    path('profesor/evaluaciones/detalle/<int:evaluacion_id>/', views.detalle_evaluacion, name='detalle_evaluacion'),
    path("dashboard/profesor/evaluaciones/<int:evaluacion_id>/quitar/<int:material_id>/", 
        views.quitar_material_evaluacion, 
        name="quitar_material_evaluacion"),


    



]

