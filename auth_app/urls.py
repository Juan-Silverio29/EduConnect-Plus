#auth_app/urls.py
from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),  # 👈 aquí está el registro
]

# auth_app/views.py
#landing/views.py
