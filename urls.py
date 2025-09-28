from django.contrib import admin
from django.urls import path, include
from resources import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),  # 👈 aquí 
    path("resources/", include("resources.urls")),
] 