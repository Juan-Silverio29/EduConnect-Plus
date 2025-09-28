from django.urls import path
from resources import views   # 👈 import absoluto para evitar warnings

urlpatterns = [
    path(
        "logros/",
        views.logros_recursos_completados,
        name="logros_recursos_completados"
    ),
]