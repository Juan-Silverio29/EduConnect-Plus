from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_recursos, name="lista_recursos"),
    path('subir/', views.subir_recurso, name="subir_recurso"),
    path('logros/', views.logros_recursos_completados, name="logros_recursos_completados"),
    path("lista/", views.lista_recursos, name="lista_recursos"),
    path("editar/<int:recurso_id>/", views.editar_recurso, name="editar_recurso"),  # 👈 importante
    path("eliminar/<int:recurso_id>/", views.eliminar_recurso, name="eliminar_recurso"),
    path("cursos/", views.lista_cursos, name="lista_cursos"),
    path("cursos/inscribirse/<int:curso_id>/", views.inscribirse_curso, name="inscribirse_curso"),

]
