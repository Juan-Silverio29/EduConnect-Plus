# auth_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Vistas normales
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("privacy/", views.privacy_policy_view, name="privacy_policy"),

    # Dashboards por rol
    path("dashboard/", views.dashboard, name="dashboard"),  # redirige según rol
    path("dashboard/estudiante/", views.estudiante_dashboard, name="dashboard_user"),
    path("dashboard/profesor/", views.profesor_dashboard, name="dashboard_profesor"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),

    # API JWT
    path("api/login/", views.api_login, name="api_login"),
    path("api/register/", views.api_register, name="api_register"),

    # API + sesión Django
    path("api/login_session/", views.api_login_session, name="api_login_session"),
    path("api/register_session/", views.api_register_session, name="api_register_session"),
]

