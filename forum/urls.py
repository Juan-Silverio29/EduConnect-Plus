from django.urls import path
from . import views

urlpatterns = [
    path("", views.foros_view, name="foros"),
]
